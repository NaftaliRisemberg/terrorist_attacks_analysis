import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class TargetType(Base):
    __tablename__ = 'target_types'

    target_type_id = Column(Integer, primary_key=True)
    target_type = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='target_types')

def create_target_type_obj(attack_data):
    return TargetType(
        target_type_id = int(uuid.uuid4()),
        target_type=attack_data['targtype1_txt']
    )