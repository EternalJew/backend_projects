from flask_api import db, app
from datetime import datetime


class PartnerLocation(db.Model):
    __tablename__ = 'partner_location'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    street_name = db.Column(db.String(30), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'), nullable=False)
    partner = db.relationship('Partner')
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __int__(self, name, partner_id, lat, lon):
        self.name = name
        self.partner_id = partner_id
        self.lat = lat
        self.lon = lon