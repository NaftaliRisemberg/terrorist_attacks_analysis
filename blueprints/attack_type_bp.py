from flask import Blueprint, jsonify, request
from services import *

attack_type_bp = Blueprint('attack_type_bp', __name__)

@attack_type_bp.route("/most_attack_type", methods=['GET'])
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


