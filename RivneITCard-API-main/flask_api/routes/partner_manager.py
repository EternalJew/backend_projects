from flask_api import db, ma, jsonify, Blueprint
from flask_restful import abort, request
from flask_api.models.partner_manager import PartnerManager
from flask_api.models.user_type import UserType
from flask_api.models.partner import Partner
from flask_api.utils.get_id_from_db_object_for_relation import get_id

main = Blueprint('partner_manager_blueprint', __name__)


class PartnerManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'phone',
                  'email', 'photo', 'type_id', 'partner_id',
                  'registered', 'auth_token')


p_manager_schema = PartnerManagerSchema()
p_manager_schema = PartnerManagerSchema(many=True)


@main.route('/', methods=['GET'])
def get_p_managers():
    all_p_managers = PartnerManager.query.all()
    result = p_manager_schema.dump(all_p_managers)

    if not result:
        abort(404, message="partner_manager exist!!")

    return jsonify(result)


@main.route('/<id>', methods=['GET'])
def get_p_manager(id):
    result = PartnerManager.query.get(id)

    if not result:
        abort(404, message="partner_manager with that 'id' exist!!")

    return jsonify(result)


@main.route('/add', methods=['POST'])
def add_p_manager():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    phone = request.json['phone']
    email = request.json['email']
    photo = request.json['photo']
    type = request.json['type']
    user_type_id = get_id(UserType, type)
    partner = request.json['partner']
    partner_id = get_id(Partner, partner)
    auth_token = request.json['auth_token']

    new_p_manager = PartnerManager(first_name, last_name, phone, email, photo, partner_id, user_type_id, auth_token)

    db.session.add(new_p_manager)
    db.session.commit()

    return p_manager_schema.jsonify(new_p_manager)


@main.route('/update/<id>', methods=['PUT'])
def update_p_manager(id):
    result = PartnerManager.query.get(id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    phone = request.json['phone']
    email = request.json['email']
    photo = request.json['photo']
    type = request.json['type']
    user_type_id = get_id(UserType, type)
    partner = request.json['partner']
    partner_id = get_id(Partner, partner)
    auth_token = request.json['auth_token']

    result.first_name = first_name
    result.last_name = last_name
    result.phone = phone
    result.email = email
    result.photo = photo
    result.user_type_id = user_type_id
    result.partner_id = partner_id
    result.auth_token = auth_token

    db.session.commit()

    return p_manager_schema.jsonify(result)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_p_manager(id):
    result = PartnerManager.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return p_manager_schema.jsonify(result)