from flask import Blueprint, abort, current_app, jsonify

regions_bp = Blueprint("regions", __name__)


@regions_bp.route("/regions", methods=["GET"])
def list_regions():
    regions = current_app.firestore.get_all_regions()
    return jsonify(regions)


@regions_bp.route("/regions/<region_id>", methods=["GET"])
def get_region(region_id):
    region = current_app.firestore.get_region(region_id)
    if not region:
        abort(404, description=f"Region '{region_id}' not found")
    return jsonify(region)
