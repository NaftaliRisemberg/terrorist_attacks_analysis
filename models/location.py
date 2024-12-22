import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Base

class Location(Base):
    __tablename__ = 'locations'

    loc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country = Column(String, nullable=False)
    city = Column(String)
    region = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='locations')

def create_location_obj(attack_data):
    return Location(
        loc_id=str(uuid.uuid4()),
        country=attack_data['country_txt'],
        city=attack_data['city'],
        region=attack_data['region_txt']
    )

