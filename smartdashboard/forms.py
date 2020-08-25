from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class Search(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Seach')

