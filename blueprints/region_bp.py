from flask import Blueprint, jsonify, request
from services import *

region_bp = Blueprint('region_bp', __name__)

@region_bp.route("/average_victims_per_events_by_region", methods=['GET'])
def get_victims_by_region():
    count = request.args.get('count', type=int)
    try:
        data = calculate_average_victims_per_event_by_region(count)

        return jsonify([{
            'region': row[0],
            'average number of victims per event': round(row[1], 3)
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

@region_bp.route("/attack_trends_by_region", methods=['GET'])
def get_percent_change_by_years():
    base_year  = request.args.get('base_year', type=int)
    compare_to_year = request.args.get('compare_to_year', type=int)
    count = request.args.get('count', type=int)

    try:
        data = calculate_percent_change(base_year, compare_to_year, count)

        return jsonify([{
            'region': row[0],
            'present': round(row[1], 3)
        } for row in data])

    except Exception as e:
        print(f"Error: {e}")

