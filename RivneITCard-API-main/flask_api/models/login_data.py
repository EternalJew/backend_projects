from flask_api import db, app
from datetime import datetime, timedelta


class LoginData(db.Model):
    __tablename__ = 'login_data'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client')
    client_email = db.Column(db.String(30), unique=True, nullable=False)
    code = db.Column(db.Integer(), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.now)
    due_time = db.Column(db.DateTime, default=datetime.now() + timedelta(hours=1))

    def __init__(self, client_id, code, client_email):
        self.client_id = client_id
        self.code = code

        self.client_email = client_email
