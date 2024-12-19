import uuid
from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from database import Base


class TerrorGroup(Base):
    __tablename__ = 'terror_groups'

    gang_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gang_name = Column(String, nullable=False)

    attacks = relationship('Attack', back_populates='terror_groups')

def create_terror_group_obj(attack_data):
    return TerrorGroup(
        gang_id = str(uuid.uuid4()),
        gang_name=attack_data['gname']
    )
