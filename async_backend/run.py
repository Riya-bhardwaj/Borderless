from app import create_app
from config import get_config

cfg = get_config()
app = create_app(cfg)

if __name__ == "__main__":
    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)
