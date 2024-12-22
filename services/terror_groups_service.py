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
        .join(TerrorGroup, Attack.terror_group_id == TerrorGroup.gang_id)
        .group_by(TerrorGroup.gang_name)
        .order_by(sum_victims.desc())
        .limit(count)
        .all()
    )
    return data
