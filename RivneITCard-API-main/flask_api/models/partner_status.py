from flask_api import db


class PartnerStatus(db.Model):
    __tablename__ = 'partner_status'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    value = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, value):
        self.name = name
        self.value = value