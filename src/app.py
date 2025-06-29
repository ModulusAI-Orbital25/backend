from flask import Flask
from flask_cors import CORS


def create_app(extra_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    app.config.from_object("config.Config")
    if extra_config is not None:
        app.config.update(extra_config)

    from auth import login_manager

    login_manager.init_app(app)
    login_manager.login_view = "auth_page.login"

    from models import db

    db.init_app(app)

    import models

    with app.app_context():
        db.drop_all()
        db.create_all()

    from profile import bp as profile_bp
    from auth import bp as auth_bp
    from chat import bp as chat_bp
    from modules import bp as modules_bp
    from sentiment import bp as sentiment_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(sentiment_bp)

    with app.app_context():
        from modules.basic import load_basic_information

        load_basic_information()

    @app.route("/")
    def index():
        return "Index page"

    return app
