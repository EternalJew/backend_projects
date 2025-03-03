from wtforms import Form, StringField, IntegerField ,SubmitField, validators
from flask_api.models.client import Client
from flask_api.models.user_type import UserType
from wtforms.validators import Regexp


class RegForm(Form):
    first_name = StringField("First Name", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="First Name must be at least 4 characters long.")
    ])
    last_name = StringField("Last Name", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="Last Name must be at least 4 characters long.")
    ])
    phone = StringField("Mobile Phone", validators=[
        validators.DataRequired(),
        validators.Length(min=10, message="Phone number must be at least 6 characters long.")
    ])
    email = StringField("E-Mail", validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(min=6, message="Email Address must be at least 6 characters long.")
    ])
    name = StringField("Type", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="Type must be at least 4 characters long.")
    ])
    submit = SubmitField("Sign Up")


    def validate_email(self, email):
        present = Client.query.filter_by(email=email.data).first()
        if present:
            raise validators.ValidationError(
                "This email has already been registered with us, please enter a different one.")

    def validate_type(self, name):
        present = UserType.query.filter_by(name=name.data).first()
        if not present:
            raise validators.ValidationError(
                "This type exist. Choose again.")


class LoginForm(Form):
    email = StringField("E-Mail", validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(min=6, message="Email Address must be at least 6 characters long.")
    ])
    code = StringField("code", validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=6)
    ])
    submit = SubmitField("Login")