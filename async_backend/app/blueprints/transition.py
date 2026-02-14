import uuid
from threading import Thread

from flask import Blueprint, abort, current_app, jsonify, request

from app.models.transition_request import validate_transition_request

transition_bp = Blueprint("transition", __name__)


@transition_bp.route("/transition", methods=["POST"])
def handle_transition():
    payload = request.get_json(force=True)
    validated = validate_transition_request(payload)

    transition_id = str(uuid.uuid4())

    # Capture references before spawning thread (current_app is request-scoped)
    engine = current_app.transition_engine

    thread = Thread(
        target=engine.process_transition,
        kwargs={
            "transition_id": transition_id,
            "user_id": validated["user_id"],
            "previous_region": validated["previous_region"],
            "current_region": validated["current_region"],
        },
        daemon=True,
    )
    thread.start()

    return jsonify({
        "status": "submitted",
        "transition_id": transition_id,
    }), 202


@transition_bp.route("/transition/<transition_id>", methods=["GET"])
def get_transition_status(transition_id):
    result = current_app.firestore.get_transition_result(transition_id)
    if not result:
        abort(404, description=f"Transition '{transition_id}' not found")
    return jsonify(result)
