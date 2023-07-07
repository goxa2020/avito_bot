from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datatypes import Base
from config import database_name, database_user, database_password, database_host, database_port
import logging

engine = create_engine(f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

logging.info('Database connect successfully')
