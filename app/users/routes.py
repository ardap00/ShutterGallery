import os
import uuid
import json
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import current_user, login_required
from app.users import users
from app.users.forms import UpdateProfileForm, UserSettingsForm
from app.models import User, PhotoPost, db, Notification
from werkzeug.utils import secure_filename
from PIL import Image

def save_avatar(form_picture):
    random_hex = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    avatar_dir = os.path.join(current_app.root_path, 'static', 'avatars')
    os.makedirs(avatar_dir, exist_ok=True)
    picture_path = os.path.join(avatar_dir, picture_fn)

    # Resize image
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    if current_app.config.get('CLOUDINARY_CLOUD_NAME'):
        import cloudinary.uploader
        try:
            upload_result = cloudinary.uploader.upload(picture_path)
            image_url = upload_result.get('secure_url')
            os.remove(picture_path)
            return image_url
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            return picture_fn

    return picture_fn

@users.route('/profile/<username>')
def profile(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if not user:
        flash('Kullanıcı bulunamadı.', 'danger')
        return redirect(url_for('main.index'))
        
    tab = request.args.get('tab', 'photos')
    posts = []
    if tab == 'photos':
        posts = db.session.execute(db.select(PhotoPost).filter_by(user_id=user.id).order_by(PhotoPost.timestamp.desc())).scalars().all()
    
    post_count = db.session.scalar(db.select(db.func.count(PhotoPost.id)).filter_by(user_id=user.id))
    
    return render_template('users/profile.html', user=user, posts=posts, tab=tab, post_count=post_count)

@users.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar_file = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        from flask_babel import _
        flash(_('Hesap bilgileriniz güncellendi!'), 'success')
        return redirect(url_for('users.account_settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    avatar_file = current_user.avatar_file if current_user.avatar_file else 'default.jpg'
    if avatar_file.startswith('http'):
        avatar_url = avatar_file
    else:
        avatar_url = url_for('static', filename='avatars/' + avatar_file)
    return render_template('users/account_settings.html', form=form, avatar_url=avatar_url)

@users.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserSettingsForm()
    if form.validate_on_submit():
        current_user.language = form.language.data
        db.session.commit()
        from flask_babel import _
        flash(_('Ayarlarınız kaydedildi!'), 'success')
        return redirect(url_for('users.settings'))
    elif request.method == 'GET':
        form.language.data = current_user.language
    
    return render_template('users/settings.html', form=form)

@users.route('/notifications')
@login_required
def notifications():
    notifications_list = current_user.notifications_received.order_by(Notification.timestamp.desc()).all()
    
    # Mark as read
    for n in notifications_list:
        if not n.is_read:
            n.is_read = True
    db.session.commit()
    
    return render_template('users/notifications.html', notifications=notifications_list)

@users.route('/follow/<username>')
@login_required
def follow(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user is None:
        flash(f'Kullanıcı bulunamadı: {username}', 'danger')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Kendinizi takip edemezsiniz!', 'warning')
        return redirect(url_for('users.profile', username=username))
    current_user.follow(user)
    
    notification = Notification(
        recipient_id=user.id,
        sender_id=current_user.id,
        type='follow'
    )
    db.session.add(notification)
    
    db.session.commit()
    flash(f'{username} adlı kullanıcıyı takip ediyorsunuz.', 'success')
    return redirect(url_for('users.profile', username=username))

@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user is None:
        flash(f'Kullanıcı bulunamadı: {username}', 'danger')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('Kendinizi takipten çıkamazsınız!', 'warning')
        return redirect(url_for('users.profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'{username} adlı kullanıcıyı takipten çıktınız.', 'info')
    return redirect(url_for('users.profile', username=username))

@users.route('/gallery/<username>')
def gallery3d(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if not user:
        flash('Kullanıcı bulunamadı.', 'danger')
        return redirect(url_for('main.index'))
        
    posts = db.session.execute(db.select(PhotoPost).filter_by(user_id=user.id).order_by(PhotoPost.timestamp.desc())).scalars().all()
    
    photos_data = []
    for post in posts:
        image_url = post.image_file if post.image_file.startswith('http') else url_for('static', filename='uploads/' + post.image_file)
        photos_data.append({
            'id': post.id,
            'title': post.title or 'İsimsiz',
            'image_url': image_url
        })
        
    return render_template('users/3d_gallery.html', user=user, photos_json=json.dumps(photos_data))
