from flask_api import db, app
from datetime import datetime


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client')
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    partner = db.relationship('Partner')
    manager_id = db.Column(db.Integer, db.ForeignKey('partner_manager.id'))
    manager = db.relationship('PartnerManager')
    transaction_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, client, partner, manager):
        self.client = client
        self.partner = partner
        self.manager = manager