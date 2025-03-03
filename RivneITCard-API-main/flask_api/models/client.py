from flask_api import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))

class Client(UserMixin, db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    photo = db.Column(BYTEA)
    client_code = db.Column(db.String(30), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)
    type = db.relationship('UserType')
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    auth_token = db.Column(db.String(300), nullable=False)

    def get_id(self):
        try:
            return self.id
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __init__(self, first_name, last_name, phone, email, photo, client_code, type_id, auth_token):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.photo = photo
        self.client_code = client_code
        self.type_id = type_id
        self.auth_token = auth_token

