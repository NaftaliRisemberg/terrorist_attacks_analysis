import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class TerrorGroup(Base):
    __tablename__ = 'terror_groups'

    gang_id = Column(Integer, primary_key=True)
    gang_name = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='terror_groups')

def create_terror_group_obj(attack_data):
    return TerrorGroup(
        gang_id = int(uuid.uuid4()),
        gang_name=attack_data['gname']
    )
