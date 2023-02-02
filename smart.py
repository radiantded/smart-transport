import requests
from config import CONTRACTOR_HOST, TOKEN, LOGGER
from datetime import datetime
from db import *
from sqlalchemy import update, insert


API_METHODS = {
    'displays': [24, Display, 'loadDisplays'],
    'display_protocols': [24, DisplayProtocol, 'loadDisplayProtocols']
}


def get_database_objects(object_type: str) -> dict:
    query = """select json_object_agg(d.contractor_id, d.id)::jsonb from(
            select contractor_id, id from smart_transport.{}) d;"""
    result = session.execute(query.format(object_type)).fetchone()[0]
    return result


def get_objects(object_type: str):
    LOGGER.info(f'{datetime.now()}: receiving {object_type}')
    
    json = {
        "t": TOKEN,
        "ct": None,
        "cd": None,
        "reg": 86002
    }

    existing_objects = get_database_objects(object_type)
    json['ct'] = API_METHODS[object_type][0]
    json['cd'] = API_METHODS[object_type][2]
    obj_class = API_METHODS[object_type][1]
    contractor_data = requests.post(CONTRACTOR_HOST, json=json).json()
    try:
        contractor_objects = contractor_data.get('data')['entities']
    except:
        LOGGER.info(f'{datetime.now()}: Нет данных')
        return
    for obj in contractor_objects:
        contractor_id = obj.get('id')
        latitude, longitude = obj.get('lat'), obj.get('lng')
        geom = f'SRID=4326;POINT({longitude} {latitude})' if latitude else None
        if existing_objects and str(contractor_id) in existing_objects:
            query = update(obj_class).where(
                obj_class.id == existing_objects[str(contractor_id)]).values(
                    geom=geom,
                    attrs=obj
                )
        else:
            query = insert(obj_class).values(
                    contractor_id=contractor_id,
                    geom=geom,
                    attrs=obj
                )
        session.execute(query)
        session.commit()


def start():
    for object_type in API_METHODS:
        get_objects(object_type)
