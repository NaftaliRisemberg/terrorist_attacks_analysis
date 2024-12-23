from flask import Blueprint, jsonify, request
from services import *

target_type_bp = Blueprint('target_type_bp', __name__)

@target_type_bp.route('/groups_with_shared_targets', methods=['GET'])
def get_groups_with_shared_targets():
    region = request.args.get('region', type=str)
    country = request.args.get('country', type=str)
    try:
        data = calculate_groups_with_shared_targets(region, country)

        all_groups = [{
            'terror group': row[0],
            'num_targets': row[1]
        } for row in data[0]]

        most_attacked_target = {
            'target type': data[1][0],
            'number groups': data[1][1]  #
        }

        return jsonify({
            'groups_with_shared_targets': all_groups,
            'target_with_most_groups': most_attacked_target
        })

    except Exception as e:
        print(f"Error: {e}")
