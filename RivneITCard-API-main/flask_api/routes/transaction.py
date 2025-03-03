from flask_api import db, ma, jsonify, Blueprint
from flask_restful import abort, request
from flask_api.models.transaction import Transaction
from flask_api.models.client import Client
from flask_api.models.partner import Partner
from flask_api.models.partner_manager import PartnerManager
from flask_api.utils.get_id_from_db_object_for_relation import get_id

main = Blueprint('transaction_blueprint', __name__)


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'client', 'partner_id', 'manager_id', 'transaction_time')


transaction_schema = TransactionSchema()
transaction_schema = TransactionSchema(many=True)


@main.route('/', methods=['GET'])
def get_transactions():
    all_transactions = Transaction.query.all()
    result = transaction_schema.dump(all_transactions)

    if not result:
        abort(404, message="transaction exist!!")

    return jsonify(result)


@main.route('/<id>', methods=['GET'])
def get_transaction(id):
    result = Transaction.query.get(id)

    if not result:
        abort(404, message="transaction with that 'id' exist!!")

    return jsonify(result)


@main.route('/add', methods=['POST'])
def add_transaction():
    client = request.json['client']
    client_id = get_id(Client, client)
    partner = request.json['partner']
    partner_id = get_id(Partner, partner)
    manager = request.json['manager']
    manager_id = get_id(PartnerManager, manager)

    new_transaction = Transaction(client_id, partner_id, manager_id)

    db.session.add(new_transaction)
    db.session.commit()

    return transaction_schema.jsonify(new_transaction)


@main.route('/update/<id>', methods=['PUT'])
def update_transaction(id):
    result = Transaction.query.get(id)
    client = request.json['client']
    client_id = get_id(Client, client)
    partner = request.json['partner']
    partner_id = get_id(Partner, partner)
    manager = request.json['manager']
    manager_id = get_id(PartnerManager, manager)

    result.client = client_id
    result.partner_id = partner_id
    result.manager_id = manager_id

    db.session.commit()

    return transaction_schema.jsonify(result)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_transaction(id):
    result = Transaction.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return transaction_schema.jsonify(result)
