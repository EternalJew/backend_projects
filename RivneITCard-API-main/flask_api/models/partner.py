from flask_api import db, app
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from sqlalchemy_utils import URLType


class Partner(db.Model):
    __tablename__ = 'partner'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    logo = db.Column(db.String(300), nullable=False)
    promo_images = db.Column(db.ARRAY(db.String), default=[])
    web_site = db.Column(URLType, nullable=False)
    locations = db.Column(db.ARRAY(db.String), default=[])
    discount = db.Column(db.String(300), nullable=False)
    d_promo_code = db.Column(db.String(50), nullable=False)
    d_value = db.Column(db.String(100), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('partner_status.id'), nullable=False)
    status = db.relationship('PartnerStatus')
    managers = db.Column(db.ARRAY(db.String), default=[])
    p_type_id = db.Column(db.Integer, db.ForeignKey('partner_type.id'), nullable=False)
    p_type = db.relationship('PartnerType')
    exclusive = db.Column(db.Boolean, default=False, nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, phone, logo, promo_images, web_site, locations, discount, d_promo_code, status_id, managers, p_type_id, exclusive, d_value):
        self.name = name
        self.phone = phone
        self.logo = logo
        self.promo_images = promo_images
        self.web_site = web_site
        self.locations = locations
        self.discount = discount
        self.d_promo_code = d_promo_code
        self.status_id = status_id
        self.managers = managers
        self.p_type_id = p_type_id
        self.exclusive = exclusive
        self.d_value = d_value