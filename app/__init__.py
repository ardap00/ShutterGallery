from flask import Flask, request, session
from flask_migrate import Migrate
from flask_babel import Babel
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.models import db, login_manager
from config import Config

migrate = Migrate()
babel = Babel()
mail = Mail()

def get_locale():
    from flask_login import current_user
    from flask import current_app
    if current_user.is_authenticated and current_user.language:
        return current_user.language
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
    mail.init_app(app)
    
    if app.config['CLOUDINARY_CLOUD_NAME']:
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET']
        )
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Lütfen bu sayfayı görüntülemek için giriş yapın.'
    login_manager.login_message_category = 'info'

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main as main_bp
    app.register_blueprint(main_bp)
    
    from app.posts import posts as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.users import users as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.messages import messages as messages_bp
    app.register_blueprint(messages_bp, url_prefix='/messages')

    # Güvenli hata işleyiciler — stack trace asla client'a gönderilmez
    @app.errorhandler(404)
    def not_found(e):
        return "<h2>404 - Sayfa Bulunamadı</h2>", 404

    @app.errorhandler(500)
    def server_error(e):
        return "<h2>500 - Sunucu Hatası</h2>", 500

    return app
