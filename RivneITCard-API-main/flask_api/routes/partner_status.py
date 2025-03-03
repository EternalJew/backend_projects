from flask_api import db, ma
from flask import jsonify, Blueprint, render_template
from flask_restful import abort, request
from flask_api.models.partner_status import PartnerStatus
from flask_api.auth_forms.partner_status import AddPartnerStatus
import pandas

main = Blueprint('partner_status', __name__)


class PartnerStatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'value')


partner_status_schema = PartnerStatusSchema()
partner_status_schema = PartnerStatusSchema(many=True)


@main.route('/get_all_partner_statuses', methods=['GET'])
def get_partner_statuses():
    statuses = PartnerStatus.query.all()
    output = []
    for status in statuses:
        status_data = {}
        status_data['id'] = status.id
        status_data['name'] = status.name
        status_data['value'] = status.value

        output.append(status_data)

    return jsonify({'types': output})


@main.route('/get_partner_status/<id>', methods=['GET'])
def get_partner_status(id):
    status = PartnerStatus.query.get(id)

    if not type:
        return {"message": "user type with that id not found"}, 404

    output = []

    status_data = {}

    status_data['id'] = status.id
    status_data['name'] = status.name
    status_data['value'] = status.value

    output.append(status_data)

    return jsonify({'partner_status': output})


@main.route('/add', methods=['GET', 'POST'])
def add_partner_status():
    form = AddPartnerStatus(request.form)
    if request.method == "POST":
        new_partner_status = PartnerStatus(name=form.name.data, value=form.value.data)
        db.session.add(new_partner_status)
        db.session.commit()

    return render_template('add_partner_status.html', form=form)

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


@main.route('/delete_partner_status/<id>', methods=['GET'])
def delete_partner_status(id):
    result = PartnerStatus.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return 200


@main.route('/upload_excel', methods=['GET'])
def upload_excel():
    return render_template('upload-excel.html')


@main.route('/uplaod_partner_statuses', methods=['POST'])
def statuses():
    if request.method == 'POST':
        file = request.files['file']
        data = pandas.read_excel(file)

        for row in data.itertuples(index=False):
            new_partner_statuses = PartnerStatus(name=row.name, value=row.value)

            db.session.add(new_partner_statuses)

        db.session.commit()

    return data.to_html()