from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class CreateContainerForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 64)])
    containername = StringField('containername', validators=[DataRequired(), Length(1, 64)])