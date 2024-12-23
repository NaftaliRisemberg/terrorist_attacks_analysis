from sqlalchemy import func
from database import session
from models import *

def calculate_groups_with_shared_targets(region=None, country=None):
    all_groups = calculate_all_groups_with_shared_targets(region, country)
    most_attacked_target = calculate_target_with_most_groups(region, country)
    return all_groups, most_attacked_target

def calculate_all_groups_with_shared_targets(region=None, country=None):
    target_count = func.count(Attack.terror_group_id).label('num_targets')

    query = (
        session.query(
            TerrorGroup.gang_name,
            target_count
        )
        .join(TerrorGroup.attacks)
        .join(Attack.locations)
    )

    if region:
        query = query.filter(Location.region == region)
    if country:
        query = query.filter(Location.country == country)

    data = (
        query
        .group_by(TerrorGroup.gang_name)
        .having(target_count > 1)
        .all()
    )
    return data


def calculate_target_with_most_groups(region=None, country=None):
    groups_count = func.count(Attack.terror_group_id).label('num_groups')

    query = (
        session.query(
            TargetType.target_type,
            groups_count
        )
        .join(Attack.target_types)
        .join(Attack.locations)
    )

    if region:
        query = query.filter(Location.region == region)
    if country:
        query = query.filter(Location.country == country)

    data = (
        query
        .group_by(TargetType.target_type)
        .order_by(groups_count.desc())
        .first()
    )
    return data

