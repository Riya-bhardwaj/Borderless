import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    # --- Secrets (from .env) ---
    FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-fallback-key")
    GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "borderless-dev")
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL_NAME = "gemini-2.5-flash"

    # --- Mode ---
    TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"
    LOCAL_STORAGE_PATH = os.environ.get("LOCAL_STORAGE_PATH", "seed_data.json")
    LOCAL_RUNTIME_PATH = os.environ.get("LOCAL_RUNTIME_PATH", "runtime_data.json")

    # --- Flask ---
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5001))
    DEBUG = False

    # --- Firestore collection names ---
    COLLECTION_REGIONS = "regions"
    COLLECTION_LIVE_UPDATES = "live_updates"
    COLLECTION_USER_SESSIONS = "user_sessions"
    COLLECTION_TRANSITION_RESULTS = "transition_results"

    # --- Alert governance ---
    MAX_ALERTS_PER_TRANSITION = 4
    DEDUP_WINDOW_HOURS = 24
    CONFIDENCE_THRESHOLD_PUSH = 0.75

    # --- Severity levels: lower number = higher priority ---
    SEVERITY_PRIORITY = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
    }

    # --- Alert category priority order (first = highest priority) ---
    ALERT_CATEGORY_PRIORITY = [
        "legal",
        "safety",
        "cultural",
        "transport",
        "language",
        "weather",
        "festival",
    ]

    # --- Live update default TTL ---
    LIVE_UPDATE_DEFAULT_TTL_HOURS = 48


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


_CONFIG_MAP = {
    "development": DevConfig,
    "production": ProdConfig,
}


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return _CONFIG_MAP.get(env, DevConfig)
