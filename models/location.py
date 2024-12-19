import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Location(Base):
    __tablename__ = 'locations'

    loc_id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='locations')

def create_location_obj(attack_data):
    return Location(
        loc_id=int(uuid.uuid4()),
        country=attack_data['country'],
        city=attack_data['city'],
        region=attack_data['region']
    )

