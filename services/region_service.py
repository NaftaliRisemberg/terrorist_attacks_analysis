from database import session
from models import *
from sqlalchemy import func

def get_victims_per_event_by_region(count):
    sum_victims = (func.sum(Attack.num_kill) + func.sum(Attack.num_wound)).label('sum_victims')
    sum_events = func.count(Attack.attack_id).label('event_count')
    average_victims_per_event = (sum_victims / sum_events).label('avg_victims_per_event')

    data = (
        session.query(
            Location.region,
            sum_victims,
        )
        .join(Location, Attack.location_id == Location.loc_id)
        .group_by(Location.region)
        .order_by(average_victims_per_event.desc())
        .limit(count)
        .all()
    )
    return data
