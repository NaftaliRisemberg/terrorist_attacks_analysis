import uuid

from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from database import Base

class TargetType(Base):
    __tablename__ = 'target_types'

    target_type_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_type = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='target_types')

def create_target_type_obj(attack_data):
    return TargetType(
        target_type_id=str(uuid.uuid4()),
        target_type=attack_data['targtype1_txt']
    )
