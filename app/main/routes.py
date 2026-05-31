from flask import render_template, request, redirect, url_for
from app.main import main
from app.models import PhotoPost, User, db

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@main.route('/search')
def search():
    q = request.args.get('q', '').strip()
    users = []
    posts = []
    if q:
        search_term = f"%{q}%"
        users = db.session.execute(db.select(User).filter(User.username.ilike(search_term))).scalars().all()
        posts = db.session.execute(
            db.select(PhotoPost).filter(
                (PhotoPost.title.ilike(search_term)) | 
                (PhotoPost.category.ilike(search_term))
            ).order_by(PhotoPost.timestamp.desc())
        ).scalars().all()
    
    return render_template('main/search_results.html', query=q, users=users, posts=posts)

from flask_login import current_user
from sqlalchemy.sql.expression import func

@main.route('/')
def index():
    if current_user.is_authenticated:
        followed_ids = [user.id for user in current_user.followed]
        followed_ids.append(current_user.id)
        
        page = request.args.get('page', 1, type=int)
        posts = db.paginate(
            db.select(PhotoPost)
            .filter(PhotoPost.user_id.in_(followed_ids))
            .order_by(PhotoPost.timestamp.desc()),
            page=page, per_page=12, error_out=False
        )
    else:
        return redirect(url_for('main.discover'))
        
    return render_template('main/index.html', posts=posts, feed_type='feed')

@main.route('/discover')
def discover():
    # Random order for discover
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(
        db.select(PhotoPost).order_by(func.random()),
        page=page, per_page=12, error_out=False
    )
    return render_template('main/index.html', posts=posts, feed_type='discover')

