from flask_api import db, ma
from flask import jsonify, Blueprint, render_template
from flask_restful import abort, request
from flask_api.models.partner_type import PartnerType
from flask_api.auth_forms.partner_type_form import AddPartnerType

main = Blueprint('partner_type', __name__)


class PartnerTypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


pType_schema = PartnerTypeSchema()
pType_schema = PartnerTypeSchema(many=True)


@main.route('/', methods=['GET'])
def get_partner_types():
    all_types = PartnerType.query.all()
    result = pType_schema.dump(all_types)

    if not result:
        abort(404, message="partner types exist!!")

    return jsonify(result)


@main.route('/<id>', methods=['GET'])
def get_partner_type(id):
    result = PartnerType.query.get(id)

    if not result:
        abort(404, message="partner type with that 'id' exist!!")

    return jsonify(result)


@main.route('/add', methods=['GET', 'POST'])
def add_partner_type():
    form = AddPartnerType(request.form)
    if request.method == "POST":
        new_partner_type = PartnerType(name=form.name.data)
        db.session.add(new_partner_type)
        db.session.commit()

    return render_template('add_partner_type.html', form=form)

@main.route('/update/<id>', methods=['PUT'])
def update_partner_type(id):
    result = PartnerType.query.get(id)
    name = request.json['name']

    result.name = name

    db.session.commit()

    return pType_schema.jsonify(result)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_partner_type(id):
    result = PartnerType.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return pType_schema.jsonify(result)