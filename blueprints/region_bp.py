from flask import Blueprint, jsonify, request
from services import *

region_bp = Blueprint('region_bp', __name__)

@region_bp.route("/victims_by_region", methods=['GET'])
def get_victims_by_region():
    count = request.args.get('count', type=int)
    try:
        data = get_victims_per_event_by_region(count)

        return jsonify([{
            'region': row[0],
            'victims': row[1]
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

