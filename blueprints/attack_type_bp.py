from flask import Blueprint, jsonify, request
from services import *

attack_type_bp = Blueprint('attack_type_bp', __name__)

@attack_type_bp.route("/most_severe_attack_types", methods=['GET'])
def get_attack_types():
    count = request.args.get('count', type=int)
    try:
        data = get_most_attack_types(count)

        return jsonify([{
            'attack_name': row[0],
            'score': row[1]
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

@attack_type_bp.route('/groups_with_shared_attack_typs', methods=['GET'])
def get_groups_with_shared_attack_typs():
    region = request.args.get('region', type=str)
    country = request.args.get('country', type=str)
    try:
        data = find_groups_with_shared_attack_types(region, country)

        all_groups = [{
            'terror group': row[0],
            'num attack types': row[1]
        } for row in data[0]]

        most_attacked_attack_types = {
            'attack type': data[1][0],
            'number groups': data[1][1]  #
        }

        return jsonify({
            'groups_with_shared_attack_types': all_groups,
            'attack_type_with_most_groups': most_attacked_attack_types
        })

    except Exception as e:
        print(f"Error: {e}")
