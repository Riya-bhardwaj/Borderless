from flask import Flask


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # --- Init services ---
    from app.services.gemini_client import GeminiClient
    from app.services.transition_engine import TransitionEngine
    from app.services.alert_governance import AlertGovernance

    if config.TEST_MODE:
        from app.services.local_file_client import LocalFileClient
        app.firestore = LocalFileClient(config)
    else:
        from app.services.firestore_client import FirestoreClient
        app.firestore = FirestoreClient(config)
    app.gemini = GeminiClient(config)
    app.governance = AlertGovernance(config)
    app.transition_engine = TransitionEngine(
        firestore=app.firestore,
        gemini=app.gemini,
        governance=app.governance,
        config=config,
    )

    # --- Register blueprints ---
    from app.blueprints.health import health_bp
    from app.blueprints.regions import regions_bp
    from app.blueprints.transition import transition_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(regions_bp, url_prefix="/api/v1")
    app.register_blueprint(transition_bp, url_prefix="/api/v1")

    # --- Register error handlers ---
    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app
