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