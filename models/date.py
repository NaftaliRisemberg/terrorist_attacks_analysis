import uuid
from datetime import date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date
from sqlalchemy.orm import relationship
from database import Base

class DateModel(Base):
    __tablename__ = 'dates'

    date_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = Column(Date, nullable=False)

    attacks = relationship('Attack', back_populates='dates')

def create_date_obj(attack_data):
    return DateModel(
        date_id=str(uuid.uuid4()),
        date=get_date(attack_data),
    )

def get_date(data):
    year = data['iyear']
    month = data['imonth']
    day = data['iday']
    return date(year, month, day)

