from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField

from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Your Email:', validators=[
                           DataRequired(), 
                           Email()])
    # message argument here allows you to specify a custom message if the user does not do what is expected of them, e.g fill a form field incorrectly
    pwd = PasswordField('Enter password:')
    
    loginbtn = SubmitField('Login')
