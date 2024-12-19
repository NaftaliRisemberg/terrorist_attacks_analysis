import uuid
from uuid import uuid4
from sqlalchemy import Column, Integer, ForeignKey, Float, String, UUID
from sqlalchemy.orm import relationship
from database import Base

class Attack(Base):
    __tablename__ = 'attacks'

    attack_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_type_id = Column(UUID(as_uuid=True), ForeignKey('target_types.target_type_id'))
    attack_type_id = Column(UUID(as_uuid=True), ForeignKey('attack_types.att_type_id'))
    num_kill = Column(Float)
    num_wound = Column(Float)
    victims = Column(Float)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey('locations.loc_id'), nullable=False)
    date_id = Column(UUID(as_uuid=True), ForeignKey('dates.date_id'))
    terror_group_id = Column(UUID(as_uuid=True), ForeignKey('terror_groups.gang_id'), nullable=False)
    num_perps = Column(Integer, nullable=False)

    target_types = relationship('TargetType', back_populates='attacks')
    attack_types = relationship('AttackType', back_populates='attacks')
    locations = relationship('Location', back_populates='attacks')
    dates = relationship('DateModel', back_populates='attacks')
    terror_groups = relationship('TerrorGroup', back_populates='attacks')

def create_attack_obj(attack_data, target_id, attack_id, location_id, date_id, terror_group_id):
    return Attack(
            attack_id=str(uuid.uuid4()),
            target_type_id=target_id,
            attack_type_id=attack_id,
            num_kill=attack_data['nkill'],
            num_wound=attack_data['nwound'],
            victims=attack_data['nkill'] + attack_data['nwound'],
            lat=attack_data['latitude'],
            long=attack_data['longitude'],
            location_id=location_id,
            date_id=date_id,
            terror_group_id=terror_group_id,
            num_perps=attack_data['nperps']
        )
