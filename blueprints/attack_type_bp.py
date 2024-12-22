from flask import Blueprint, jsonify, request
from services import *

attack_type_bp = Blueprint('attack_type_bp', __name__)

@attack_type_bp.route("/most_attack_type", methods=['GET'])
def get_attack_types():
    count = request.args.get('count', type=int)
    try:
        data = get_most_attack_types(count)

        return jsonify([{
            'attack_name': attack_type[0],
            'score': attack_type[1]
        } for attack_type in data])

    except Exception as e:
        print(f"Error: {e}")


