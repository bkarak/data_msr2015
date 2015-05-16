from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from conf.configuration import Configuration

# initialise database
# TODO: fix the configuration file issue
configuration = Configuration('config.json')

import internals

internals.engine = create_engine(configuration.get_database_url())
internals.base = declarative_base(bind=internals.engine)
internals.Session = sessionmaker(autocommit=False, autoflush=False, bind=internals.engine)

import models
