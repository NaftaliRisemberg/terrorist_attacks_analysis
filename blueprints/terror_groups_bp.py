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

@terror_groups_bp.route("/most_active_groups", methods=['GET'])
def get_most_active_groups_by_region():
    region = request.args.get('region', type=str)
    try:
        data = calculate_most_active_groups(region)

        return jsonify([{
            'terror group name': row[0],
            'attacks number': row[1]
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

@terror_groups_bp.route("/groups_shared_attacks", methods=['GET'])
def get_terror_groups_involved_in_same_attack():
    try:
        data = find_terror_groups_involved_in_same_attack()

        return jsonify(data)

    except Exception as e:
        print(f"Error: {e}")
