from flask_api import db
from datetime import datetime


class ClientCompany(db.Model):
    __tablename__ = 'client_company'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name=name