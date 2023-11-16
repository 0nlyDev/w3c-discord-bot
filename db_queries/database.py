import json

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def get_engine(config_path='./configs/config.json'):
    with open(config_path, 'r') as file:
        data = json.load(file)
    connection_string = ('mysql+pymysql://'
                         f"{data['db_username']}:"
                         f"{data['db_password']}@"
                         f"{data['db_host']}:"
                         f"{data['db_port']}/"
                         f"{data['db_name']}")
    engine = create_engine(connection_string)
    return engine


def initialize_database(engine):
    Base.metadata.create_all(engine)


def create_session(engine):
    session = sessionmaker(bind=engine)
    return session()
