from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from app.models import User, db

class UpdateProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    bio = TextAreaField('Biyografi', validators=[Length(max=200)])
    avatar = FileField('Profil Fotoğrafı Güncelle', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
            if user:
                raise ValidationError('Bu kullanıcı adı alınmış. Lütfen başka bir tane seçin.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
            if user:
                raise ValidationError('Bu e-posta adresi zaten kullanımda.')
