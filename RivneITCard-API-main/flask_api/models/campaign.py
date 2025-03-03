from flask_api import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import BYTEA


class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    promo_image = db.Column(BYTEA)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('partner_manager.id'))
    created_by = db.relationship('PartnerManager')

    def __init__(self, name, description, promo_image, from_date, to_date, created_by_id):
        self.name = name
        self.description = description
        self.promo_image = promo_image
        self.from_date = from_date
        self.to_date = to_date
        self.created_by_id = created_by_id
