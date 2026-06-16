from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    body = TextAreaField('Mesaj', validators=[DataRequired(), Length(min=1, max=1000)])
    submit = SubmitField('Gönder')
