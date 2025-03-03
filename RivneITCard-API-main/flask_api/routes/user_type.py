from flask_api import db, ma, app
from flask import jsonify, Blueprint, render_template
from flask_restful import abort, request
from flask_api.models.user_type import UserType
from flask_api.auth_forms.user_type_form import AddUserType
import pandas

main = Blueprint('user_type', __name__)


class UserTypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


uType_schema = UserTypeSchema()
uType_schema = UserTypeSchema(many=True)


@main.route('/get_all', methods=['GET'])
def get_user_types():
    types = UserType.query.all()
    output = []
    for type in types:
        type_data = {}
        type_data['id'] = type.id
        type_data['name'] = type.name

        output.append(type_data)

    return jsonify({'types': output})


@main.route('/get/<id>', methods=['GET'])
def get_user_type(id):
    type = UserType.query.get(id)

    if not type:
        return {"message": "user type with that id not found"}, 404

    output = []

    type_data = {}

    type_data['id'] = type.id
    type_data['name'] = type.name

    output.append(type_data)

    return jsonify({'user_type': output})


@main.route('/add', methods=['GET', 'POST'])
def add_user_type():
    form = AddUserType(request.form)
    if request.method == "POST":
        new_user_type = UserType(name=form.name.data)
        db.session.add(new_user_type)
        db.session.commit()

    return render_template('add_user_type.html', form=form)

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


@main.route('/delete/<id>', methods=['DELETE'])
def delete_user_type(id):
    result = UserType.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return uType_schema.jsonify(result)


@main.route('/upload_excel', methods=['GET'])
def upload_excel():
    return render_template('upload-excel.html')


@main.route('/upload', methods=['POST'])
def upload_user_types():
    if request.method == 'POST':
        file = request.files['file']
        data = pandas.read_excel(file)

        for row in data.itertuples(index=False):
            new_type = UserType(name=row.name)

            db.session.add(new_type)

        db.session.commit()

    return data.to_html()