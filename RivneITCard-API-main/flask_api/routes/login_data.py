from flask_api import db, ma, jsonify, Blueprint
from flask_restful import abort, request
from flask_api.models.login_data import LoginData
from flask_api.models.client import Client
from flask_api.utils.get_id_from_db_object_for_relation import get_name_from_type, get_id_from_email
import random
from datetime import date

main = Blueprint('login_data', __name__)


class LoginDataSchema(ma.Schema):
     class Meta:
         fields = ('id', 'client_id', 'code')


login_data_schema = LoginDataSchema()
login_data_schema = LoginDataSchema(many=True)

@main.route('/get_codes', methods=['GET'])
def get_codes():
    codes = LoginData.query.all()
    output = []
    for code in codes:
        code_data = {}
        code_data['id'] = code.id
        code_data['code'] = code.code
        #code_data['client_name'] = get_name_from_type(Client, code.client_id)
        code_data['email'] = code.email
        code_data['due_time'] = code.due_time

        output.append(code_data)

    return jsonify({'codes': output})



@main.route('/add_login_code', methods=['GET', 'POST'])
def add_code(email):
 #gen code and add all to db
     new_code = LoginData(
         client_id=get_id_from_email(Client, email),
         code=gen_code(),
         client_email=email,
     )

     db.session.add(new_code)
     db.session.commit()

     return {"message": "code created and added"}


def gen_code():
     code = ''.join(str(random.randint(0, 9)) for _ in range(6))
     return code


def check_time():
     codes = LoginData.query.all()

     for code in codes:
         return 0