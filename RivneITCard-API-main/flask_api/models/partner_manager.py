from flask_api import db, app
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA


class PartnerManager(db.Model):
    __tablename__ = 'partner_manager'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    photo = db.Column(BYTEA)
    type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)
    type = db.relationship('UserType')
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)
    partner = db.relationship('Partner')
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    auth_token = db.Column(db.String(300), nullable=False)

    def __init__(self, first_name, last_name, phone, email, photo, type_id, auth_token, partner_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.photo = photo
        self.type_id = type_id
        self.auth_token = auth_token
        self.partner_id = partner_id
