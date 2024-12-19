from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Base
from database.config import POSTGRES_URL

engine = create_engine(POSTGRES_URL)
DBSession = sessionmaker(autocommit=False,
                        autoflush=False,
                        bind=engine)

Session = scoped_session(DBSession)
session = Session()

def init_db():
    import models
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

init_db()