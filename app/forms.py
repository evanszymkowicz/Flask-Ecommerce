# Makes our forms more modular. We will not throw everything inside our app file
from flas_wtf import FlaskForm
from wtfforms import StringField, PasswordField, BooleanField, Submitfield
from wtfforms.validators import DataRequired, Email, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired, Email])
    password = PasswordField()
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    f_name = StringField("First Name")
    l_name = StringField("Last Name")
    username = StringField("Username")
    Email = StringField ("Email")
    password = PasswordField ("Password")
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField("Register")

    def validate(self, email):
        user = User.query.filter_by(username=.data).first()
        if user is not None:
            
