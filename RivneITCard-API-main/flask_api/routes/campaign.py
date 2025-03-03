from flask_api import db, ma, jsonify, Blueprint
from flask_restful import abort, request
from flask_api.models.campaign import Campaign
from flask_api.models.partner_manager import PartnerManager
from flask_api.utils.get_id_from_db_object_for_relation import get_id

main = Blueprint('campaign_blueprint', __name__)


class CampaignSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'promo_image', 'from_date', 'to_date', 'created', 'created_by_id')


campaign_schema = CampaignSchema()
campaign_schema = CampaignSchema(many=True)


@main.route('/', methods=['GET'])
def get_campaigns():
    campaigns = Campaign.query.all()
    output = []
    for campaign in campaigns:
        campaign_data = {}
        campaign_data['id'] = campaign.id
        campaign_data['name'] = campaign.name
        campaign_data['description'] = campaign.description
        campaign_data['promo_image'] = campaign.promo_image
        campaign_data['from_date'] = campaign.from_date.strftime('%Y-%m-%d')
        campaign_data['to_date'] = campaign.to_date.strftime('%Y-%m-%d')
        campaign_data['created_by'] = campaign.created_by
        output.append(campaign_data)

    return jsonify({'campaigns': output})


@main.route('/<id>', methods=['GET'])
def get_campaign(id):
    result = Campaign.query.get(id)

    if not result:
        abort(404, message="campaign with that 'id' exist!!")

    return jsonify(result)


@main.route('/add', methods=['POST'])
def add_campaign():
    data = request.get_json()
    new_campaign = Campaign(name=data['name'],
                            description=data['description'],
                            promo_image=data['promo_image'],
                            from_date=data['from_date'],
                            to_date=data['to_date'],
                            created_by=data['created_by']) #add get id func

    db.session.add(new_campaign)
    db.session.commit()

    return campaign_schema.jsonify(new_campaign)


@main.route('/update/<id>', methods=['PUT'])
def update_campaign(id):
    result = Campaign.query.get(id)

    name = request.json['name']
    description = request.json['description']
    promo_image = request.json['promo_image']
    from_date = request.json['from_date']
    to_date = request.json['to_date']
    created_by = request.json['created_by']
    created_by_id = get_id(PartnerManager, created_by)

    result.name = name
    result.description = description
    result.promo_image = promo_image
    result.from_date = from_date
    result.to_date = to_date
    result.created_by_id = created_by_id


    db.session.commit()

    return campaign_schema.jsonify(result)


@main.route('/delete/<id>', methods=['DELETE'])
def delete_campaign(id):
    result = Campaign.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return campaign_schema.jsonify(result)
