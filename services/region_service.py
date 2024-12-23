from database import session
from models import *
from sqlalchemy import func, case

def calculate_average_victims_per_event_by_region(count):
    sum_victims = (func.sum(Attack.num_kill) + func.sum(Attack.num_wound)).label('sum_victims')
    sum_events = func.count(Attack.attack_id).label('event_count')
    average_victims_per_event = (sum_victims / sum_events).label('avg_victims_per_event')

    data = (
        session.query(
            Location.region,
            average_victims_per_event,
        )
        .join(Attack.locations)
        .group_by(Location.region)
        .order_by(average_victims_per_event.desc())
        .limit(count)
        .all()
    )
    return data

def calculate_percent_change(base_year, compare_to_year, count):
    year = func.extract('year', DateModel.date).label('year')
    base_year_count = func.count(Attack.attack_id).filter(year == base_year).label('base_year_count')
    compare_to_year_count = func.count(Attack.attack_id).filter(year == compare_to_year).label('compare_to_year_count')
    change_percent = case((base_year_count != 0, compare_to_year_count - base_year_count * 100 / base_year_count),else_=100)

    data = (
        session.query(
            Location.region,
            change_percent
        )
        .join(Attack.locations)
        .join(Attack.dates)
        .filter(year.in_([base_year, compare_to_year]))
        .group_by(Location.region)
        .order_by(change_percent.desc())
        .limit(count)
        .all()
    )
    return data






