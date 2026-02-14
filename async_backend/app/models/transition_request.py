from app.errors import ValidationError

_REQUIRED_FIELDS = ["previous_region", "current_region", "user_id"]


def validate_transition_request(payload):
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object")

    for field in _REQUIRED_FIELDS:
        if field not in payload or not payload[field]:
            raise ValidationError(f"Missing required field: '{field}'")

    return {
        "previous_region": str(payload["previous_region"]),
        "current_region": str(payload["current_region"]),
        "user_id": str(payload["user_id"]),
    }
