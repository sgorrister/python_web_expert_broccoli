from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class FeedbackForm(FlaskForm):
    name = StringField('Імя', validators=[DataRequired()])
    feedback_text = TextAreaField('Відгук', validators=[DataRequired()])
    liked = BooleanField('Чи сподобався вам сайт?')
