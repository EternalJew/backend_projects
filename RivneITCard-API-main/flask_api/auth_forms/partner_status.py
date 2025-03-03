from wtforms import Form, StringField, IntegerField ,SubmitField, validators
from flask_api.models.client import Client
from flask_api.models.user_type import UserType


class AddPartnerStatus(Form):
    name = StringField("Partner Status", validators=[
        validators.DataRequired(),
        validators.Length(min=4, message="partner status name must be at least 4 characters long.")
    ])
    value = IntegerField("Value", validators=[
        validators.DataRequired(),
        validators.Length(min=1, message="value must be at least 1 characters long.")
    ])
    submit = SubmitField("Add")