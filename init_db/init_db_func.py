import pandas as pd
from models import *
from database.connection import session
from models.date import get_date

def read_csv(file_path, fields):
    df_ = pd.read_csv(file_path,
                     skipinitialspace=True,
                     usecols=fields,
                     encoding='latin1') \
            .drop_duplicates(keep='first', inplace=False)
    return df_

def get_or_create(table_class, search_fields, create_func):
    obj = session.query(table_class).filter_by(**search_fields).first()

    if obj:
        return obj
    else:
        try:
            new_obj = create_func()
            add_objects_to_db(new_obj)
            return new_obj
        except Exception as e:
            print(f"Error creating {table_class.__name__}: {e}")
            return None

def create_db_objects(data):
    attack_type_obj = get_or_create(AttackType, {'attack_type': data['attacktype1_txt']}, lambda: create_attack_type_obj(data))
    attack_type_id = attack_type_obj.att_type_id

    date_obj = get_or_create(DateModel, {'date': get_date(data)}, lambda: create_date_obj(data))
    date_id = date_obj.date_id

    location_obj = get_or_create(Location, {
        'country': data['country_txt'],
        'city': data['city'],
        'region': data['region_txt']
    }, lambda: create_location_obj(data))
    location_id = location_obj.loc_id

    target_type_obj = get_or_create(TargetType, {'target_type': data['targtype1_txt']}, lambda: create_target_type_obj(data))
    target_type_id = target_type_obj.target_type_id

    terror_group_obj = get_or_create(TerrorGroup, {'gang_name': data['gname']}, lambda: create_terror_group_obj(data))
    terror_group_id = terror_group_obj.gang_id

    attack_obj = create_attack_obj(data, target_type_id, attack_type_id, location_id, date_id, terror_group_id)
    add_objects_to_db(attack_obj)

    return attack_type_id, date_id, location_id, target_type_id, terror_group_id, attack_obj

def add_objects_to_db(*objects):
    try:
        for obj in objects:
            session.add(obj)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding objects to session: {e}")
