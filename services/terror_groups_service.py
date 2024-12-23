from database import session
from models import *
from sqlalchemy import func

def get_most_damaging_terror_groups(count):
    sum_victims = (func.sum(Attack.num_kill) + func.sum(Attack.num_wound)).label('sum_victims')
    data = (
        session.query(
            TerrorGroup.gang_name,
            sum_victims,
        )
        .join(TerrorGroup.attacks)
        .group_by(TerrorGroup.gang_name)
        .order_by(sum_victims.desc())
        .limit(count)
        .all()
    )
    return data

def calculate_most_active_groups(region=None):
    sum_attacks = func.count(Attack.attack_id).label('sum_attacks')
    query = (
        session.query(
            TerrorGroup.gang_name,
            sum_attacks
        )
        .join(Attack.terror_groups)
        .join(Attack.locations)
    )

    if region:
        query = query.filter(Location.region == region)

    data = (
        query
        .group_by(TerrorGroup.gang_name)
        .order_by(sum_attacks.desc())
        .all()
    )
    return data

def find_terror_groups_involved_in_same_attack():
    subquery = (
        session.query(
            Attack.location_id,
            Attack.date_id,
            func.count(Attack.attack_id).label('attack_count')
        )
        .group_by(Attack.location_id, Attack.date_id)
        .having(func.count(Attack.attack_id) > 1)
        .subquery()
    )

    data = (
        session.query(
            Attack.attack_id,
            TerrorGroup.gang_name,
            Attack.location_id,
            Attack.date_id
        )
        .join(Attack.terror_groups)
        .join(Attack.locations)
        .join(Attack.dates)
        .filter(Attack.location_id == subquery.c.location_id)
        .filter(Attack.date_id == subquery.c.date_id)
        .all()
    )

    result = {}
    for row in data:
        event_key = f"{row.location_id}_{row.date_id}"
        gang_name = row.gang_name
        if event_key not in result:
            result[event_key] = []
        if gang_name not in result[event_key]:
            result[event_key].append(gang_name)
        elif gang_name == "Unknown":
            result[event_key].append("Unknown")

    filtered_result = {event_key: gangs for event_key, gangs in result.items() if len(gangs) > 2}
    return filtered_result
