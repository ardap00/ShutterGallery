import os
import uuid
from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, User, Game, GameRound
from app.game import game
from app.game.ai_judge import get_random_theme, judge_round

def _generate_room_code():
    return uuid.uuid4().hex[:6].upper()

def _save_game_photo(file_storage):
    """
    Saves an uploaded photo either to Cloudinary (if configured) or locally to uploads folder.
    Returns the saved filename or Cloudinary URL.
    """
    filename = secure_filename(file_storage.filename)
    unique_filename = f"game_{uuid.uuid4().hex}_{filename}"
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    picture_path = os.path.join(upload_dir, unique_filename)
    file_storage.save(picture_path)

    if current_app.config.get('CLOUDINARY_CLOUD_NAME'):
        import cloudinary.uploader
        try:
            upload_result = cloudinary.uploader.upload(picture_path)
            image_url = upload_result.get('secure_url')
            try:
                os.remove(picture_path)
            except OSError:
                pass
            return image_url
        except Exception as e:
            print(f"Game photo Cloudinary upload failed: {e}")
            return unique_filename
    return unique_filename

@game.route('/lobby')
@login_required
def lobby():
    # Active waiting games that the user can join
    waiting_games = db.session.execute(
        db.select(Game).filter(
            Game.status == 'waiting',
            Game.player1_id != current_user.id
        ).order_by(Game.created_at.desc()).limit(10)
    ).scalars().all()

    # User's current active game if any
    active_game = db.session.execute(
        db.select(Game).filter(
            (Game.player1_id == current_user.id) | (Game.player2_id == current_user.id),
            Game.status.in_(['waiting', 'in_progress'])
        ).order_by(Game.created_at.desc())
    ).scalars().first()

    return render_template('game/lobby.html', waiting_games=waiting_games, active_game=active_game)

@game.route('/create', methods=['POST'])
@login_required
def create_game():
    # Cancel any previous waiting game of this user
    old_games = db.session.execute(
        db.select(Game).filter(
            Game.player1_id == current_user.id,
            Game.status == 'waiting'
        )
    ).scalars().all()
    for g in old_games:
        g.status = 'cancelled'

    room_code = _generate_room_code()
    first_theme = get_random_theme()

    new_game = Game(
        room_code=room_code,
        player1_id=current_user.id,
        status='waiting',
        target_score=3,
        current_round_num=1
    )
    db.session.add(new_game)
    db.session.flush()

    first_round = GameRound(
        game_id=new_game.id,
        round_num=1,
        theme=first_theme['theme'],
        theme_description=first_theme['desc'],
        status='uploading'
    )
    db.session.add(first_round)
    db.session.commit()

    return redirect(url_for('game.arena', room_code=room_code))

@game.route('/join/<code>', methods=['GET', 'POST'])
@login_required
def join_game(code):
    game_obj = db.session.execute(
        db.select(Game).filter_by(room_code=code.upper())
    ).scalar_one_or_none()

    if not game_obj:
        flash('Oyun odası bulunamadı.', 'error')
        return redirect(url_for('game.lobby'))

    if game_obj.player1_id == current_user.id:
        return redirect(url_for('game.arena', room_code=game_obj.room_code))

    if game_obj.player2_id and game_obj.player2_id != current_user.id:
        flash('Bu oda zaten dolu!', 'error')
        return redirect(url_for('game.lobby'))

    if not game_obj.player2_id:
        game_obj.player2_id = current_user.id
        game_obj.status = 'in_progress'
        db.session.commit()

    return redirect(url_for('game.arena', room_code=game_obj.room_code))

@game.route('/arena/<code>')
@login_required
def arena(code):
    game_obj = db.session.execute(
        db.select(Game).filter_by(room_code=code.upper())
    ).scalar_one_or_none()

    if not game_obj:
        flash('Oyun odası bulunamadı.', 'error')
        return redirect(url_for('game.lobby'))

    if current_user.id not in [game_obj.player1_id, game_obj.player2_id]:
        flash('Bu oyun odasına erişim izniniz yok.', 'error')
        return redirect(url_for('game.lobby'))

    current_round = db.session.execute(
        db.select(GameRound).filter_by(
            game_id=game_obj.id,
            round_num=game_obj.current_round_num
        )
    ).scalar_one_or_none()

    is_player1 = (current_user.id == game_obj.player1_id)

    return render_template(
        'game/arena.html',
        game=game_obj,
        round=current_round,
        is_player1=is_player1
    )

@game.route('/api/status/<code>')
@login_required
def game_status(code):
    game_obj = db.session.execute(
        db.select(Game).filter_by(room_code=code.upper())
    ).scalar_one_or_none()

    if not game_obj:
        return jsonify({'error': 'Oyun bulunamadı'}), 404

    current_round = db.session.execute(
        db.select(GameRound).filter_by(
            game_id=game_obj.id,
            round_num=game_obj.current_round_num
        )
    ).scalar_one_or_none()

    p1 = game_obj.player1
    p2 = game_obj.player2

    # Check if both uploaded and round is ready to be judged
    if current_round and current_round.status == 'uploading':
        if current_round.player1_image and current_round.player2_image:
            current_round.status = 'judging'
            db.session.commit()
            
            # Execute judging synchronously or trigger it
            result = judge_round(
                theme_name=current_round.theme,
                theme_desc=current_round.theme_description or '',
                p1_username=p1.username if p1 else 'Oyuncu 1',
                p1_img=current_round.player1_image,
                p2_username=p2.username if p2 else 'Oyuncu 2',
                p2_img=current_round.player2_image
            )

            current_round.ai_reasoning = result.get('reasoning')
            current_round.ai_feedback_p1 = result.get('feedback_p1')
            current_round.ai_feedback_p2 = result.get('feedback_p2')
            current_round.status = 'completed'

            winner_str = result.get('winner')
            if winner_str == 'player1':
                current_round.winner_id = game_obj.player1_id
                game_obj.player1_score += 1
            elif winner_str == 'player2' and game_obj.player2_id:
                current_round.winner_id = game_obj.player2_id
                game_obj.player2_score += 1
            else:
                current_round.is_tie = True

            # Check if anyone won the game (target score: 3)
            if game_obj.player1_score >= game_obj.target_score:
                game_obj.status = 'completed'
                game_obj.winner_id = game_obj.player1_id
            elif game_obj.player2_score >= game_obj.target_score:
                game_obj.status = 'completed'
                game_obj.winner_id = game_obj.player2_id
            
            db.session.commit()

    round_data = None
    if current_round:
        round_data = {
            'id': current_round.id,
            'round_num': current_round.round_num,
            'theme': current_round.theme,
            'theme_description': current_round.theme_description,
            'status': current_round.status,
            'p1_uploaded': bool(current_round.player1_image),
            'p2_uploaded': bool(current_round.player2_image),
            'p1_image': current_round.player1_image if current_round.status == 'completed' else None,
            'p2_image': current_round.player2_image if current_round.status == 'completed' else None,
            'winner_id': current_round.winner_id,
            'is_tie': current_round.is_tie,
            'reasoning': current_round.ai_reasoning,
            'feedback_p1': current_round.ai_feedback_p1,
            'feedback_p2': current_round.ai_feedback_p2
        }

    return jsonify({
        'status': game_obj.status,
        'current_round_num': game_obj.current_round_num,
        'target_score': game_obj.target_score,
        'p1_score': game_obj.player1_score,
        'p2_score': game_obj.player2_score,
        'p1': {
            'id': p1.id,
            'username': p1.username,
            'avatar': p1.avatar_file
        } if p1 else None,
        'p2': {
            'id': p2.id,
            'username': p2.username,
            'avatar': p2.avatar_file
        } if p2 else None,
        'winner_id': game_obj.winner_id,
        'current_user_id': current_user.id,
        'round': round_data
    })

@game.route('/api/upload/<code>', methods=['POST'])
@login_required
def upload_photo(code):
    game_obj = db.session.execute(
        db.select(Game).filter_by(room_code=code.upper())
    ).scalar_one_or_none()

    if not game_obj:
        return jsonify({'error': 'Oyun bulunamadı'}), 404

    if current_user.id not in [game_obj.player1_id, game_obj.player2_id]:
        return jsonify({'error': 'İzniniz yok'}), 403

    current_round = db.session.execute(
        db.select(GameRound).filter_by(
            game_id=game_obj.id,
            round_num=game_obj.current_round_num
        )
    ).scalar_one_or_none()

    if not current_round or current_round.status != 'uploading':
        return jsonify({'error': 'Bu tur için fotoğraf yükleme kapalı'}), 400

    if 'photo' not in request.files:
        return jsonify({'error': 'Fotoğraf seçilmedi'}), 400

    file = request.files['photo']
    if not file or file.filename == '':
        return jsonify({'error': 'Geçersiz dosya'}), 400

    saved_url = _save_game_photo(file)

    now = datetime.now(timezone.utc)
    if current_user.id == game_obj.player1_id:
        current_round.player1_image = saved_url
        current_round.player1_uploaded_at = now
    else:
        current_round.player2_image = saved_url
        current_round.player2_uploaded_at = now

    db.session.commit()
    return jsonify({'success': True, 'image_url': saved_url})

@game.route('/api/next_round/<code>', methods=['POST'])
@login_required
def next_round(code):
    game_obj = db.session.execute(
        db.select(Game).filter_by(room_code=code.upper())
    ).scalar_one_or_none()

    if not game_obj:
        return jsonify({'error': 'Oyun bulunamadı'}), 404

    if game_obj.status == 'completed':
        return jsonify({'error': 'Oyun tamamlandı'}), 400

    current_round = db.session.execute(
        db.select(GameRound).filter_by(
            game_id=game_obj.id,
            round_num=game_obj.current_round_num
        )
    ).scalar_one_or_none()

    if not current_round or current_round.status != 'completed':
        return jsonify({'error': 'Mevcut tur henüz tamamlanmadı'}), 400

    # Advance round if next round doesn't already exist
    next_round_num = game_obj.current_round_num + 1
    existing_next = db.session.execute(
        db.select(GameRound).filter_by(
            game_id=game_obj.id,
            round_num=next_round_num
        )
    ).scalar_one_or_none()

    if not existing_next:
        used_themes = [r.theme for r in game_obj.rounds]
        new_theme = get_random_theme(used_themes)

        new_round = GameRound(
            game_id=game_obj.id,
            round_num=next_round_num,
            theme=new_theme['theme'],
            theme_description=new_theme['desc'],
            status='uploading'
        )
        db.session.add(new_round)
        game_obj.current_round_num = next_round_num
        db.session.commit()

    return jsonify({'success': True, 'next_round': next_round_num})
