from prepare_data_2 import formating_df
from init_db_func import create_db_objects, read_csv
from clear_data import clear_all

def init_db(file_path, fields, need_prepare=False):
    data = read_csv(file_path, fields)
    if need_prepare:
        data = formating_df(data)
    clear_data = clear_all(data)

    counter = 0
    try:
        for index, row in clear_data.iterrows():
            attack_type_id, date_id, location_id, target_type_id, terror_group_id, attack_obj = create_db_objects(row)
            if attack_type_id and date_id and location_id and target_type_id and terror_group_id and attack_obj:
                counter += 1
                print(f'still working, counter: {counter}')
            else:
                print("error")
        return "data inserted successfully"
    except Exception as e:
        print(f"Error processing message: {e}")

fields_data_1 = ['nkill', 'nwound', 'nperps', 'longitude', 'latitude', 'attacktype1_txt',
          'country_txt', 'city', 'iyear', 'imonth', 'iday', 'region_txt', 'gname', 'targtype1_txt']
data_path_1 = '../data/globalterrorismdb_0718dist-1000 rows.csv'

fields_data_2 = ['Date', 'City', 'Country',	'Perpetrator', 'Weapon', 'Injuries', 'Fatalities', 'Description']
data_path_2 = '../data/RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv'

#init_db(data_path_2, fields_data_2, need_prepare=True)
#init_db(data_path_1, fields_data_1, need_prepare=False)