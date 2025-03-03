
def get_id(model_class, name_from_json):
    obj_from_db = model_class.query.filter_by(name=name_from_json).first()
    if obj_from_db is not None:
        id = obj_from_db.id

    return id


def get_name_from_type(model_class, id):
    obj_from_db = model_class.query.filter_by(id=id).first()
    if obj_from_db is not None:
        name = obj_from_db.name

    return name


def get_id_from_email(model_class, email):
    obj_from_db = model_class.query.filter_by(email=email).first()
    if obj_from_db is not None:
        id = obj_from_db.id

    return id
