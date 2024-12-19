import pandas as pd
from models import *
from database.connection import session

fields = ['nkill', 'nwound', 'nperps', 'longitude', 'latitude', 'attacktype1_txt',
          'country_txt', 'city', 'iyear', 'imonth', 'iday', 'region_txt', 'gname']

df = pd.read_csv('../data/globalterrorismdb.csv', skipinitialspace=True, usecols=fields, encoding='latin1')

def create_db_objects(data):
        attack_type_obj = create_attack_type_obj(data)
        attack_id = attack_type_obj.att_type_id

        date_obj = create_date_obj(data)
        date_id = date_obj.date_id

        location_obj = create_location_obj(data)
        location_id = location_obj.loc_id

        target_type_obj = create_target_type_obj(data)
        target_id = target_type_obj.target_type_id

        terror_group_obj = create_terror_group_obj(data)
        terror_group_id = terror_group_obj.gang_id

        attack_obj = create_attack_obj(data, attack_id, date_id, location_id, target_id, terror_group_id)

        add_objects_to_db( attack_type_obj, date_obj, location_obj, target_type_obj, terror_group_obj, attack_obj)

        return attack_type_obj, date_obj, location_obj, target_type_obj, terror_group_obj, attack_obj

def add_objects_to_db(*objects):
    try:
        for obj in objects:
            session.add(obj)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding objects to session: {e}")

def init_db(data):
    try:
        attack_type_obj, date_obj, location_obj, target_type_obj, terror_group_obj, attack_obj = create_db_objects(data)

        add_objects_to_db(attack_type_obj, date_obj, location_obj, target_type_obj, terror_group_obj, attack_obj)

    except Exception as e:
        print(f"Error processing message: {e}")
