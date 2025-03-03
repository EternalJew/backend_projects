from flask_api import db
from datetime import datetime


class ClientAllowedDomains(db.Model):
    __tablename__ = 'client_allowed_domains'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    domain = db.Column(db.String(30), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('client_company.id'), nullable=False)
    partner = db.relationship('ClientCompany')
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, domain, partner_id):
        self.domain = domain
        self.partner_id = partner_id