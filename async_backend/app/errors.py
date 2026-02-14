from flask import jsonify


class ValidationError(Exception):
    pass


class RegionNotFoundError(Exception):
    pass


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": "validation_error", "message": str(e)}), 400

    @app.errorhandler(RegionNotFoundError)
    def handle_not_found(e):
        return jsonify({"error": "not_found", "message": str(e)}), 404

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "not_found", "message": e.description}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "internal_error", "message": "An unexpected error occurred"}), 500
