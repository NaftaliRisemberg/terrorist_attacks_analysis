from sqlalchemy import func
from database import session
from models import *

def get_most_attack_types(count):
    sum_score = (func.sum(Attack.num_kill) * 2 + func.sum(Attack.num_wound)).label('sum_score')
    data = (
        session.query(
            AttackType.attack_type,
            sum_score
        )
        .join(Attack.attack_types)
        .group_by(AttackType.attack_type)
        .order_by(sum_score.desc())
        .limit(count)
        .all()
    )
    return data

def find_groups_with_shared_attack_types(region=None, country=None):
    all_groups = find_all_groups_with_shared_attack_types(region, country)
    most_attacked_attack = find_attack_typs_with_most_groups(region, country)
    return all_groups, most_attacked_attack

def find_all_groups_with_shared_attack_types(region=None, country=None):
    attack_type_count = func.count(Attack.terror_group_id).label('attack_type_count')

    query = (
        session.query(
            TerrorGroup.gang_name,
            attack_type_count
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
        .having(attack_type_count > 1)
        .all()
    )
    return data

def find_attack_typs_with_most_groups(region=None, country=None):
    groups_count = func.count(Attack.terror_group_id).label('num_groups')

    query = (
        session.query(
            AttackType.attack_type,
            groups_count
        )
        .join(Attack.attack_types)
        .join(Attack.locations)
    )

    if region:
        query = query.filter(Location.region == region)
    if country:
        query = query.filter(Location.country == country)

    data = (
        query
        .group_by(AttackType.attack_type)
        .order_by(groups_count.desc())
        .first()
    )
    return data
