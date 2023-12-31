from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Todo')
