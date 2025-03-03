from flask_api import db, ma, jsonify, Blueprint, app
from flask import render_template
from flask_restful import abort, request
from flask_api.models.partner_location import PartnerLocation
from flask_api.models.partner import Partner
from flask_api.models.partner_type import PartnerType
from flask_api.utils.get_id_from_db_object_for_relation import get_id, get_name_from_type
from flask_api.auth_forms.partner_form import LocationForm
from flask_api.auth_forms.partner_location_form import PartnerLocationForm

main = Blueprint('partner_location', __name__)


class PartnerLocationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street_name', 'partner', 'lat', 'lon')


p_location_schema = PartnerLocationSchema()
p_location_schema = PartnerLocationSchema(many=True)


@main.route('/get_locations', methods=['GET'])
def get_p_locations():
    locations = PartnerLocation.query.all()
    output = []
    for location in locations:
        loc_data = {}
        loc_data['id'] = location.id
        loc_data['street_name'] = location.name
        loc_data['partner_name'] = get_name_from_type(Partner, location.partner_id)
        loc_data['lat'] = location.lat
        loc_data['lon'] = location.lon

        output.append(loc_data)

    return jsonify({'locations': output})


@main.route('/location/<id>', methods=['GET'])
def get_p_location(id):
    location = PartnerLocation.query.get(id)

    if not location:
        abort(404, message="partner_location with that 'id' exist!!")

    output = []

    loc_data = {}

    loc_data['id'] = location.id
    loc_data['street_name'] = location.name
    loc_data['partner_name'] = get_name_from_type(Partner, location.partner_id)
    loc_data['lat'] = location.lat
    loc_data['lon'] = location.lon

    return jsonify({'location': output})


@main.route('/add', methods=['GET', 'POST'])
def add_p_location():
    form = LocationForm(request.form)
    if request.method == "POST" and form.validate():
        new_p_location = PartnerLocation(street_name=form.street_name.data,
                                         lat=form.lat.data,
                                         lon=form.lon.data,
                                         partner_id=get_id(Partner, form.partner.data)
                                         )
    db.session.add(new_p_location)
    db.session.commit()

    return render_template('add_location.html', form=form)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_p_location(id):
    result = PartnerLocation.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return p_location_schema.jsonify(result)


@main.route('/partner_locations', methods=['GET'])
def get_partner_locations():
     list = db.session.query(PartnerLocation.street_name, PartnerLocation.lat, PartnerLocation.lon).all()

     formatted_list = [{'name': _list.street_name, 'lat': _list.lat, 'lon': _list.lon} for _list in list]

     return jsonify(formatted_list)


@main.route('/sort_by_type', methods=['GET', 'POST'])
def sort_by_partner_type():
    partner_type_name = request.form.get('type')

    # Пошук типу партнера за назвою в таблиці partner_type
    partner_type = PartnerType.query.filter_by(name=partner_type_name).first()

    if partner_type:
        # Отримання ID знайденого типу партнера
        partner_type_id = partner_type.id

        # Пошук партнерів, що мають співпадіння знайденого ID типу партнера
        partners = Partner.query.filter_by(p_type_id=partner_type_id).all()

        # Формування списку партнерів з додатковою інформацією
        partner_list = []
        for partner in partners:
            partner_data = {
                'name': partner.name,
                'phone': partner.phone,
                'logo': partner.logo,
                # Додайте інші необхідні поля

                # Отримання інформації про розташування партнера
                'locations': []
            }

            # Пошук розташування партнера за його ID в таблиці partner_location
            partner_locations = PartnerLocation.query.filter_by(partner_id=partner.id).all()

            for location in partner_locations:
                location_data = {
                    'street_name': location.street_name,
                    'lat': location.lat,
                    'lon': location.lon
                }
                partner_data['locations'].append(location_data)

            partner_list.append(partner_data)

        return jsonify(partner_list), 200

    return jsonify({'error': 'Partner type not found'}), 404
    #return render_template('sort_loc.html')


@main.route('/sort_by_typee', methods=['GET', 'POST'])
def sort_by_partner_typee():
    partner_type_name = request.form.get('type')

    # Пошук типу партнера за назвою в таблиці partner_type
    partner_type = PartnerType.query.filter_by(name=partner_type_name).first()

    if partner_type:
        # Отримання ID знайденого типу партнера
        partner_type_id = partner_type.id

        # Пошук партнерів, що мають співпадіння знайденого ID типу партнера
        partners = Partner.query.filter_by(p_type_id=partner_type_id).all()

        # Формування списку партнерів з додатковою інформацією
        partner_list = []
        for partner in partners:
            partner_data = {
                'name': partner.name,
                'phone': partner.phone,
                'logo': partner.logo,
                # Додайте інші необхідні поля

                # Отримання інформації про розташування партнера
                'locations': []
            }

            # Пошук розташування партнера за його ID в таблиці partner_location
            partner_locations = PartnerLocation.query.filter_by(partner_id=partner.id).all()

            for location in partner_locations:
                location_data = {
                    'street_name': location.street_name,
                    'lat': location.lat,
                    'lon': location.lon
                }
                partner_data['locations'].append(location_data)

            partner_list.append(partner_data)

        return jsonify(partner_list), 200

    #return jsonify({'error': 'Partner type not found'}), 404
    return render_template('sort_loc.html')


import pandas
from fileinput import filename
# Root endpoint
# @app.get('/upload_excel')
# def upload():
#     return render_template('upload-excel.html')
#
#
# @app.post('/upload_partner_locs')
# def upload_partner_locations():
#     if request.method == 'POST':
#         # Read the File using Flask request
#         file = request.files['file']
#         # Save file in local directory
#         file.save(file.filename)
#
#         # Parse the data as a Pandas DataFrame type
#         data = pandas.read_excel(file)
#
#         # Iterate over the rows in the DataFrame and insert them into the database
#         for row in data.itertuples(index=False):
#             new_location = PartnerLocation(
#                 name=row.name,
#                 lat=row.lat,
#                 lon=row.lon,
#                 partner_id=get_id(Partner, row.partner_name)
#                 )
#             db.session.add(new_location)
#
#         # Commit the changes to the database
#         db.session.commit()
#
#         # Return HTML snippet that will render the table
#         return data.to_html()
