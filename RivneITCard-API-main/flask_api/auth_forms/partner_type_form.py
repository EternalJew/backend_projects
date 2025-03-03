from wtforms import Form, StringField, IntegerField ,SubmitField, validators
from flask_api.models.client import Client
from flask_api.models.user_type import UserType


class AddPartnerType(Form):
    name = StringField("Partner Type Name", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="type name must be at least 4 characters long.")
    ])
    submit = SubmitField("Add")