from flask_api.models.partner import Partner
from wtforms import Form, StringField, BooleanField, FloatField, IntegerField, FieldList, SubmitField, FormField, validators
from wtforms.validators import NumberRange, URL, DataRequired
from flask_api.models.partner_manager import PartnerManager

class LocationForm(Form):
    #location = StringField('Location', validators=[DataRequired()])
    street_name = StringField('Street Name', validators=[DataRequired()])
    partner = StringField('Partner Name', validators=[DataRequired()])
    lat = FloatField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    lon = FloatField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180)])


class ManagerForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), validators.Email()])
    user_type = StringField('User Type', validators=[DataRequired()])
    partner_name = StringField('Partner Name', validators=[DataRequired()])

    def validate_email(self, email):
        present = PartnerManager.query.filter_by(email=email.data).first()
        if present:
            raise validators.ValidationError(
                "This email has already been registered with us, please enter a different one.")


class PartnerForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    logo = StringField('Logo', validators=[DataRequired()])
    promo_images = FieldList(StringField('Promo Images'), min_entries=3)
    web_site = StringField('Website', validators=[DataRequired(), URL()])
    locations = FieldList(FormField(LocationForm), min_entries=2)
    discount = StringField('Discount', validators=[DataRequired()])
    d_promo_code = StringField('Discount Promocode', validators=[DataRequired()])
    d_value = StringField('Discount Value', validators=[DataRequired()])
    status = StringField('Status ID', validators=[DataRequired()])
    managers = FieldList(FormField(ManagerForm), min_entries=2)
    type_name = StringField('Partner Type ID', validators=[DataRequired()])
    exclusive = BooleanField('Exclusive', default=False)
    submit = SubmitField("Sign Up")






