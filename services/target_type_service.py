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

def find_groups_with_shared_targets_same_year(year):
    year_expr = func.extract('year', DateModel.date).label('attack_year')

    subquery = (
        session.query(
            Attack.target_type_id,
            year_expr,
            func.count(Attack.terror_group_id).label('group_count')
        )
        .join(Attack.dates)
        .group_by(Attack.target_type_id, year_expr)
        .having(func.count(Attack.terror_group_id) > 1)
        .subquery()
    )

    query = (
        session.query(
            TerrorGroup.gang_name,
            Attack.target_type_id,
            year_expr
        )
        .join(Attack.terror_groups)
        .join(Attack.target_types)
        .join(Attack.dates)
        .filter(Attack.target_type_id == subquery.c.target_type_id)
        .filter(year_expr == subquery.c.attack_year)
    )

    if year:
        query = query.filter(year_expr == year)

    data = query.all()

    result = {}
    for row in data:
        gang_name = row.gang_name
        target_type_id = str(row.target_type_id)
        attack_year = int(row.attack_year)

        if attack_year not in result:
            result[attack_year] = {}
        if target_type_id not in result[attack_year]:
            result[attack_year][target_type_id] = []

        result[attack_year][target_type_id].append(gang_name)

    return result
