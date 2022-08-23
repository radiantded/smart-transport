from geoalchemy2.types import Geometry
from sqlalchemy import JSON, Column, Integer, MetaData, String, create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import CreateSchema

from config import DB_HOST, DB_NAME, DB_PORT, DB_PWD, DB_USER, LOGGER


ENGINE = create_engine(
    f'postgresql+psycopg2://'
    f'{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_pre_ping=True,
    client_encoding='utf8'
)

def init_db():
    try:
        ENGINE.execute(CreateSchema('smart_transport'))
    except ProgrammingError:
        LOGGER.info('Schema already exists, skipping...')

    metadata_obj.create_all(ENGINE)


metadata_obj = MetaData(schema='smart_transport')
Base = declarative_base(metadata=metadata_obj)
Base.metadata.bind = ENGINE
session = sessionmaker(bind=ENGINE)()


class Display(Base):
    __tablename__ = 'displays'
    id = Column(Integer, primary_key=True)
    contractor_id = Column(String, comment='Идентификатор поставщика данных')
    geom = Column(Geometry('POINT', srid=4326))
    attrs = Column(MutableDict.as_mutable(JSON), comment='Другие данные')
    

class DisplayProtocol(Base):
    __tablename__ = 'display_protocols'
    id = Column(Integer, primary_key=True)
    contractor_id = Column(String, comment='Идентификатор поставщика данных')
    geom = Column(Geometry('POINT', srid=4326))
    attrs = Column(MutableDict.as_mutable(JSON), comment='Другие данные')
