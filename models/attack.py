import uuid
from uuid import uuid4

from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

class Attack(Base):
    __tablename__ = 'attacks'

    attack_id = Column(Integer, primary_key=True)
    target_type_id = Column(Integer, ForeignKey('target_types.target_type_id'))
    attack_type_id = Column(Integer, ForeignKey('attack_types.att_type_id'))
    num_kill = Column(Integer, nullable=False)
    num_wound = Column(Integer, nullable=False)
    victims = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.loc_id'), nullable=False)
    date_id = Column(Integer, ForeignKey('dates.date_id'))
    terror_group_id = Column(Integer, ForeignKey('terror_groups.gang_id'), nullable=False)
    num_perps = Column(Integer, nullable=False)

    target_type = relationship('TargetType', back_populates='attacks')
    attack_type = relationship('AttackType', back_populates='attacks')
    location = relationship('Location', back_populates='attacks')
    date = relationship('DateModel', back_populates='attacks')
    terror_group = relationship('TerrorGroup', back_populates='attacks')

def create_attack_obj(attack_data, target_id, attack_id, location_id, date_id, terror_group_id):
    return Attack(
            attack_id=int(uuid.uuid4()),
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
