from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ


def create_app(extra_config=None):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=[environ.get("FRONTEND_URL")])
    app.config.from_object("config.Config")
    if extra_config is not None:
        app.config.update(extra_config)

    from auth import login_manager

    login_manager.init_app(app)
    login_manager.login_view = "auth_page.login"

    from models import db

    db.init_app(app)

    import models

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    from profile import bp as profile_bp
    from auth import bp as auth_bp
    from chat import bp as chat_bp
    from modules import bp as modules_bp
    from sentiment import bp as sentiment_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(modules_bp)
    app.register_blueprint(sentiment_bp)

    print(app.url_map)

    with app.app_context():
        from modules.basic import load_basic_information

        load_basic_information()

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify(
            {
                "error": "Not Found",
                "path": request.path,
                "method": request.method,
                "message": f"The endpoint {request.path} does not exist.",
            }
        ), 404

    @app.route("/")
    def index():
        return "Index page"

    return app
