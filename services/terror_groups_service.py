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

