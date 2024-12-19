import uuid
from datetime import date
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base

class DateModel(Base):
    __tablename__ = 'dates'

    date_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)

    attacks = relationship('Attack', back_populates='dates')

def create_date_obj(attack_data):
    return DateModel(
        date_id=int(uuid.uuid4()),
        date=get_date(attack_data),
    )

def get_date(data):
    year = data['iyear']
    month = data['imonth']
    day = data['iday']
    return date(year, month, day)

