from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL


class PartnerLocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    #lon
    #lat
    #partner
    submit = SubmitField('Submit')