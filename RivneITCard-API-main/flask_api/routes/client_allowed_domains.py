from flask_api import db, ma
from flask import jsonify, Blueprint, render_template
from flask_restful import abort, request
from flask_api.models.client_allowed_domains import ClientAllowedDomains
from flask_api.utils.get_id_from_db_object_for_relation import get_id, get_name_from_type
from flask_api.models.partner import Partner
import pandas

main = Blueprint('client_allowed_domains', __name__)


class ClientAllowedDomainsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'domains', 'partner')


client_allowed_domains_schema = ClientAllowedDomainsSchema()
client_allowed_domains_schema = ClientAllowedDomainsSchema(many=True)


@main.route('/get_all', methods=['GET'])
def get_all_domains():
    domains = ClientAllowedDomains.query.all()
    output = []
    for domain in domains:
        domain_data = {}
        domain_data['id'] = domain.id
        domain_data['domains'] = domain.domains
        domain_data['partner'] = get_name_from_type(Partner, domain.partner_id)

        output.append(domain_data)

    return jsonify({'domains': output})


@main.route('/get_one/<id>', methods=['GET'])
def get_domain(id):
    domain = ClientAllowedDomains.query.get(id)

    if not type:
        return {"message": "user type with that id not found"}, 404

    output = []

    domain_data = {}
    domain_data['id'] = domain.id
    domain_data['domains'] = domain.domains
    domain_data['partner'] = get_name_from_type(Partner, domain.partner_id)

    output.append(domain_data)

    return jsonify({'domain': output})


@main.route('/add_new_domain', methods=['POST'])
def add_domain():
    form = AddDomain(request.form)
    if request.method == "POST" and form.validate():
        new_domain = ClientAllowedDomains(domain=form.domain.data, partner_id=get_id(Partner, form.domain.data))
        db.session.add(new_domain)
        db.session.commit()

    return {"message": "add client company success"}, 200

# @main.route('/update/<id>', methods=['PUT'])
# def update_user_type(id):
#     result = UserType.query.get(id)
#     name = request.json['name']
#
#     result.name = name
#
#     db.session.commit()
#
#     return uType_schema.jsonify(result)


@main.route('/delete_domain/<id>', methods=['DELETE'])
def delete_domain(id):
    result = ClientAllowedDomains.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return client_allowed_domains_schema.jsonify(result)


@main.route('/upload_excel', methods=['GET'])
def upload_excel():
    return render_template('upload-excel.html')


@main.route('/upload_client_company', methods=['POST'])
def add_domains():
    if request.method == 'POST':
        file = request.files['file']
        data = pandas.read_excel(file)

        for row in data.itertuples(index=False):
            new_domains = ClientAllowedDomains(domain=row.domain,
                                               partner_id=get_id(Partner, row.partner))

            db.session.add(new_domains)

        db.session.commit()

    return data.to_html()