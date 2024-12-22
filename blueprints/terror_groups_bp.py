from flask import Blueprint, jsonify, request
from services import *

terror_groups_bp = Blueprint('terror_groups_bp', __name__)

@terror_groups_bp.route("/most_damaging_groups", methods=['GET'])
def get_most_damaging_groups():
    count = request.args.get('count', type=int)
    try:
        data = get_most_damaging_terror_groups(count)

        return jsonify([{
            'terror group name': row[0],
            'victims': row[1]
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

