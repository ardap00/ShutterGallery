from flask import render_template, request, redirect, url_for
from app.main import main
from app.models import PhotoPost, User, db

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
        
        posts = db.session.execute(
            db.select(PhotoPost)
            .filter(PhotoPost.user_id.in_(followed_ids))
            .order_by(PhotoPost.timestamp.desc())
        ).scalars().all()
    else:
        return redirect(url_for('main.discover'))
        
    return render_template('main/index.html', posts=posts, feed_type='feed')

@main.route('/discover')
def discover():
    # Random order for discover
    posts = db.session.execute(db.select(PhotoPost).order_by(func.random())).scalars().all()
    return render_template('main/index.html', posts=posts, feed_type='discover')

@main.route('/gallery')
def gallery():
    posts = db.session.execute(db.select(PhotoPost).order_by(PhotoPost.timestamp.desc())).scalars().all()
    return render_template('main/gallery.html', posts=posts)
