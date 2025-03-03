from flask_login import LoginManager
from flask import Flask, jsonify, current_app, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)

# postgresql://oleksii:1310526879@localhost:5432/test - dev
# postgresql://itcard:itcard@itcard_db_postgresql:5432/itcard - prod

app.config["SECRET_KEY"] = '55555'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://itcard:itcard@itcard_db_postgresql:5432/itcard'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
ma = Marshmallow(app)
db.init_app(app)

###LOGIN/REGISTER###

from flask_bootstrap import Bootstrap

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

from .routes import client, user_type, partner_type, partner_manager, partner_location, partner, campaign, transaction, partner_status, client_company, client_allowed_domains, login_data

app.register_blueprint(client.main, url_prefix='/api/client')
app.register_blueprint(user_type.main, url_prefix='/api/user_type')
app.register_blueprint(partner_type.main, url_prefix='/api/partner_type')
app.register_blueprint(partner_manager.main, url_prefix='/api/partner_manager')
app.register_blueprint(partner_location.main, url_prefix='/api/partner_location')
app.register_blueprint(partner.main, url_prefix='/api/partner')
app.register_blueprint(campaign.main, url_prefix='/api/campaign')
app.register_blueprint(transaction.main, url_prefix='/api/transaction')
app.register_blueprint(partner_status.main, url_prefix='/api/partner_status')
app.register_blueprint(client_company.main, url_prefix='/api/client_company')
app.register_blueprint(client_allowed_domains.main, url_prefix='/api/domain')
app.register_blueprint(login_data.main, url_prefix='/api/code')


def delete_all_records():
    with app.app_context():
        # Очищення всіх таблиць в базі даних
        db.drop_all()

        # Повторне створення таблиць
        db.create_all()

        # Запуск COMMIT для підтвердження змін
        db.session.commit()

        print("Всі записи в базі даних були видалені.")


# Виклик функції для видалення всіх записів з бази даних
#delete_all_records()
