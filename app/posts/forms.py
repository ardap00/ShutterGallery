from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class PhotoPostForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    description = TextAreaField('Açıklama', validators=[Optional()])
    category = SelectField('Kategori', choices=[
        ('Doga', 'Doğa'),
        ('Sokak', 'Sokak'),
        ('Mimari', 'Mimari'),
        ('Portre', 'Portre'),
        ('Astrofotografi', 'Astrofotoğrafi'),
        ('Diger', 'Diğer')
    ], validators=[DataRequired()])
    
    image_file = FileField('Fotoğraf Yükle', validators=[
        FileRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece görsel dosyaları yüklenebilir.')
    ])
    
    camera_model = StringField('Kamera Modeli', validators=[Optional()])
    lens_model = StringField('Lens Modeli', validators=[Optional()])
    iso = IntegerField('ISO', validators=[Optional()])
    aperture = StringField('Diyafram (örn: f/2.8)', validators=[Optional()])
    shutter_speed = StringField('Enstantane (örn: 1/250)', validators=[Optional()])
    editing_software = StringField('Düzenleme Yazılımı', validators=[Optional()])
    
    submit = SubmitField('Paylaş')

class CommentForm(FlaskForm):
    body = TextAreaField('Yorumunuz', validators=[DataRequired()])
    submit = SubmitField('Gönder')
