import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class AttackType(Base):
    __tablename__ = 'attack_types'

    att_type_id = Column(Integer, primary_key=True)
    attack_type = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='attack_types')

def create_attack_type_obj(attack_data):
    return AttackType(
        att_type_id = int(uuid.uuid4()),
        attack_type=attack_data['attacktype1_txt']
    )
