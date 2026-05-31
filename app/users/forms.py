from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_login import current_user
from flask_babel import lazy_gettext as _l
from app.models import User, db

class UpdateProfileForm(FlaskForm):
    username = StringField(_l('Kullanıcı Adı'), validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField(_l('E-posta'), validators=[DataRequired(), Email()])
    bio = TextAreaField(_l('Biyografi'), validators=[Length(max=200)])
    avatar = FileField(_l('Profil Fotoğrafı Güncelle'), validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField(_l('Güncelle'))

    def validate_username(self, username):
        if username.data != current_user.username:
            user = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
            if user:
                raise ValidationError(_l('Bu kullanıcı adı alınmış. Lütfen başka bir tane seçin.'))

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
            if user:
                raise ValidationError(_l('Bu e-posta adresi zaten kullanımda.'))

class UserSettingsForm(FlaskForm):
    language = SelectField(_l('Dil'), choices=[('tr', 'Türkçe'), ('en', 'English')])
    submit = SubmitField(_l('Kaydet'))

