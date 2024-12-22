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


def get_attack_trends_by_region(base_year, compare_to_year, count):
    year = func.extract('year', DateModel.date_id).label('year')
    attack_count = func.count(Attack.attack_id).label('attack_count')

    data = (
        session.query(
            Location.region,
            attack_count,
            year
        )
        .join(Location, Attack.location_id == Location.loc_id)
        .join(DateModel, Attack.date_id == DateModel.date_id)
        .filter(year.in_([base_year, compare_to_year]))
        .group_by(Location.region, year)
        .order_by(Location.region)
        .all()
    )

    region_trends = {}

    for region, attack_count, year in data:
        if region not in region_trends:
            region_trends[region] = {}
        region_trends[region][year] = attack_count

    percentage_changes = []
    for region, years in region_trends.items():
        if base_year in years and compare_to_year in years:
            start_count = years[base_year]
            end_count = years[compare_to_year]
            if start_count != 0:
                percentage_change = ((end_count - start_count) / start_count) * 100
                percentage_changes.append((region, percentage_change))

    return percentage_changes