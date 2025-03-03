from wtforms import Form, StringField, IntegerField ,SubmitField, validators
from flask_api.models.client import Client
from flask_api.models.user_type import UserType


class AddClientCompany(Form):
    name = StringField("Client Company", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="client company name must be at least 4 characters long.")
    ])
    submit = SubmitField("Add")