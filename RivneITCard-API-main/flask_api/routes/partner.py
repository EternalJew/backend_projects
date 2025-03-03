from flask_api import db, ma, jsonify, Blueprint, app, cross_origin
from flask import render_template
from flask_restful import abort, request
from flask_api.models.partner import Partner
from flask_api.models.partner_type import PartnerType
from flask_api.models.user_type import UserType
from flask_api.models.partner_status import PartnerStatus
from flask_api.utils.get_id_from_db_object_for_relation import get_id, get_name_from_type
from flask_api.auth_forms.partner_form import PartnerForm
from flask_api.models.partner_location import PartnerLocation
from flask_api.models.partner_manager import PartnerManager
from datetime import datetime

main = Blueprint('partner', __name__)


class PartnerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'logo',
                  'promo_images', 'web_site', 'locations', 'discount',
                  'd_promo_code', 'd_value', 'status_id',
                  'managers', 'p_type_id', 'exclusive', 'registered')


partner_schema = PartnerSchema()
partner_schema = PartnerSchema(many=True)


@main.route('/get_partners', methods=['GET'])
def get_partners():
    partners = Partner.query.all()
    output = []
    for partner in partners:
        partner_data = {}
        partner_data['id'] = partner.id
        partner_data['name'] = partner.name
        partner_data['phone'] = partner.phone
        partner_data['logo'] = partner.logo
        partner_data['promo_images'] = partner.promo_images
        partner_data['web_site'] = partner.web_site
        partner_data['locations'] = partner.locations
        partner_data['discount'] = partner.discount
        partner_data['d_promo_code'] = partner.d_promo_code
        partner_data['d_value'] = partner.d_value
        partner_data['status_name'] = get_name_from_type(PartnerStatus, partner.status_id)
        partner_data['managers'] = partner.managers
        partner_data['type_name'] = get_name_from_type(PartnerType, partner.p_type_id)
        partner_data['exclusive'] = partner.exclusive
        partner_data['registered'] = partner.registered

        output.append(partner_data)

    return jsonify({'partners': output})


@main.route('/partners_list', methods=['GET'])
@cross_origin()
def partner_list():

     list = db.session.query(Partner.name, Partner.phone, Partner.logo, Partner.web_site).all()#add promo_images

     formatted_list = [{'name': _list.name, 'phone': _list.phone, 'logo': _list.logo, 'url': _list.web_site} for _list in list]

     return jsonify(formatted_list)


@main.route('/<id>', methods=['GET'])
def get_partner(id):
    partner = Partner.query.get(id)

    if not partner:
        abort(404, message="partner with that 'id' exist!!")

    output = []

    partner_data = {}

    partner_data['id'] = partner.id
    partner_data['name'] = partner.name
    partner_data['phone'] = partner.phone
    partner_data['logo'] = partner.logo
    partner_data['promo_images'] = partner.promo_images
    partner_data['web_site'] = partner.web_site
    partner_data['locations'] = partner.locations
    partner_data['discount'] = partner.discount
    partner_data['d_promo_code'] = partner.d_promo_code
    partner_data['d_value'] = partner.d_value
    partner_data['status_name'] = get_name_from_type(PartnerStatus, partner.status_id)
    partner_data['managers'] = partner.managers
    partner_data['type_name'] = get_name_from_type(PartnerType, partner.p_type_id)
    partner_data['exclusive'] = partner.exclusive
    partner_data['registered'] = partner.registered

    output.append(partner_data)

    return jsonify({'partner': output})


@main.route('/add', methods=['GET', 'POST'])
def add_partner():
    form = PartnerForm(request.form)
    if request.method == "POST" and form.validate():
        phone = form.phone.data
        if phone.startswith("+38"):
            phone = phone[3:]  # Видаляємо перші 3 символи (+38)

        _phone = Partner.query.filter_by(phone=phone).first()
        if _phone:
            return render_template('add_partner.html', form=form)

        new_partner = Partner(name=form.name.data,
                              phone=phone,
                              logo=form.logo.data,
                              promo_images=form.promo_images.data,
                              web_site=form.web_site.data,
                              locations=[location.street_name.data for location in form.locations],
                              discount=form.discount.data,
                              d_promo_code=form.d_promo_code.data,
                              d_value=form.d_value.data,
                              status_id=get_id(PartnerStatus, form.status.data),
                              managers=[manager.first_name.data for manager in form.managers],
                              p_type_id=get_id(PartnerType, form.type_name.data),
                              exclusive=form.exclusive.data
                              )
        db.session.add(new_partner)
        db.session.commit()

        for location in form.locations:
            partner_location = PartnerLocation(street_name=location.street_name.data,
                                               partner_id=new_partner.id,
                                               lat=location.lat.data,
                                               lon=location.lon.data
                                               )
            db.session.add(partner_location)
        db.session.commit()

        for manager in form.managers:
            new_manager = PartnerManager(first_name=manager.first_name.data,
                                         last_name=manager.last_name.data,
                                         phone=manager.phone.data,
                                         email=manager.email.data,
                                         photo=None,
                                         type_id=get_id(UserType, manager.user_type.data),
                                         partner_id=get_id(Partner, manager.partner_name.data),
                                         auth_token=''
                                         )
            db.session.add(new_manager)
        db.session.commit()

    return render_template('add_partner.html', form=form)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_partner(id):
    result = Partner.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return {"message": "partner successfully deleted"}, 200


from sqlalchemy import func
@main.route('/cards', methods=['GET', 'POST'])
def partner_card():
    sort_by = request.args.get('sort_by')
    if sort_by == 'date':
        # Сортування за датою подачі
        cards = db.session.query(Partner.name, Partner.d_value).order_by(Partner.registered).all()
        print(cards)
        #return jsonify({'date': cards})
    elif sort_by == 'discount':
        # Сортування за розміром знижки
        cards = db.session.query(Partner.name, Partner.d_value).order_by(Partner.d_value.desc()).all()
        print(cards)
        #return jsonify({'discount': cards})
    else:
        # Без сортування
        cards = db.session.query(Partner.name, Partner.d_value).order_by(func.random()).all()
        formatted_cards = [{'d_value': card.d_value, 'name': card.name} for card in cards]
        return jsonify(formatted_cards)


    #return render_template('cards.html', cards=cards)

import pandas
from pandas import read_excel


@main.route('/upload_partners', methods=['GET', 'POST'])
def upload_partners_from_excel():
    if request.method == 'GET':
        # Render the upload form
        return render_template('upload-excel.html')
    elif request.method == 'POST':
        # Read the File using Flask request
        file = request.files['file']
        # Save file in local directory
        file.save(file.filename)

        partner_data = read_excel(file, sheet_name="partners")
        location_data = read_excel(file, sheet_name="locations")
        manager_data = read_excel(file, sheet_name="managers")

        for index, row in partner_data.iterrows():
            partner_street_names = location_data[location_data['partner'] == row['name']]['street_name'].tolist()
            partner_manager_names = manager_data[manager_data['partner'] == row['name']]['email'].tolist()
            new_partner = Partner(name=row['name'],
                                  phone=row.phone,
                                  logo=row.logo,
                                  promo_images=row.promo_images,
                                  web_site=row.web_site,
                                  locations=partner_street_names,
                                  discount=row.discount,
                                  d_promo_code=row.promo_code,
                                  d_value=row.value,
                                  status_id=get_id(PartnerStatus, row.status),
                                  managers=partner_manager_names,
                                  p_type_id=get_id(PartnerType, row.type),
                                  exclusive=row.exclusive
                                  )
            db.session.add(new_partner)
        db.session.commit()

        for index, location_row in location_data.iterrows():
            partner_location = PartnerLocation(street_name=location_row['street_name'],
                                               partner_id=get_id(Partner, location_row.partner),
                                               lat=location_row.lat,
                                               lon=location_row.lon
                                               )
            db.session.add(partner_location)
        db.session.commit()

        for index, manager_row in manager_data.iterrows():
            new_manager = PartnerManager(first_name=manager_row['first_name'],
                                         last_name=manager_row.last_name,
                                         phone=manager_row.phone,
                                         email=manager_row.email,
                                         photo=None,
                                         type_id=get_id(UserType, manager_row.user_type),
                                         partner_id=get_id(Partner, manager_row.partner),
                                         auth_token=''
                                         )
            db.session.add(new_manager)
        db.session.commit()
    return 'Partners uploaded successfully!'



