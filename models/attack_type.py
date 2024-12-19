import uuid
from sqlalchemy import Column, Integer, String, BigInteger, UUID
from sqlalchemy.orm import relationship
from database import Base

class AttackType(Base):
    __tablename__ = 'attack_types'

    att_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attack_type = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='attack_types')

def create_attack_type_obj(attack_data):
    return AttackType(
        att_type_id = str(uuid.uuid4()),
        attack_type=attack_data['attacktype1_txt']
    )
