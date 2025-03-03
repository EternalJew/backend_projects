from flask_api import db, ma
from flask import jsonify, Blueprint, render_template
from flask_restful import abort, request
from flask_api.models.client_company import ClientCompany
from flask_api.auth_forms.client_company_form import AddClientCompany
import pandas

main = Blueprint('clientcompany_blueprint', __name__)


class ClientCompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


client_company_schema = ClientCompanySchema()
client_company_schema = ClientCompanySchema(many=True)


@main.route('/get_all_client_companies', methods=['GET'])
def get_client_companies():
    companies = ClientCompany.query.all()
    output = []
    for company in companies:
        company_data = {}
        company_data['id'] = company.id
        company_data['name'] = company.name

        output.append(company_data)

    return jsonify({'companies': output})


@main.route('/get_client_company/<id>', methods=['GET'])
def get_client_company(id):
    client_company = ClientCompany.query.get(id)

    if not type:
        return {"message": "user type with that id not found"}, 404

    output = []

    company_data = {}

    company_data['id'] = client_company.id
    company_data['name'] = client_company.name


    output.append(company_data)

    return jsonify({'client_company': output})

@main.route('/add_new_client_company', methods=['POST'])
def add_client_company():
    form = AddClientCompany(request.form)
    if request.method == "POST" and form.validate():
        new_client_company = ClientCompany(name=form.name.data)
        db.session.add(new_client_company)
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


@main.route('/delete_client_company/<id>', methods=['DELETE'])
def delete_client_company(id):
    result = ClientCompany.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return client_company_schema.jsonify(result)


@main.route('/upload_excel', methods=['GET'])
def upload_excel():
    return render_template('upload-excel.html')


@main.route('/upload_client_company', methods=['POST'])
def client_companies():
    if request.method == 'POST':
        file = request.files['file']
        data = pandas.read_excel(file)

        for row in data.itertuples(index=False):
            new_client_companies = ClientCompany(name=row.name)

            db.session.add(new_client_companies)

        db.session.commit()

    return data.to_html()