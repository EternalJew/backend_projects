from flask_api import db, app


class PartnerType(db.Model):
    __tablename__ = 'partner_type'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        self.name = name


