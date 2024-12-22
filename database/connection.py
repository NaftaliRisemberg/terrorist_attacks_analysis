from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Base
import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv('POSTGRES_URL')

engine = create_engine(POSTGRES_URL)
DBSession = sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=engine)

Session = scoped_session(DBSession)
session = Session()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)

init_db()