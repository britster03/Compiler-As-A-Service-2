# backend/app.py

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from config import config
from models import db
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/codex.log', maxBytes=10240, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Compiler as a Service startup')

def create_app():
    # Determine the configuration to use
    config_name = os.getenv('FLASK_ENV', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    CORS(app)
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)
    
    # Conditional HTTPS enforcement
    if config_name == 'production':
        Talisman(app, content_security_policy=None, force_https=True)
    else:
        Talisman(app, content_security_policy=None, force_https=False)
    
    setup_logging(app)

    # Metrics
    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Compiler as a Service API', version='1.0.0')

    # Register blueprints
    from api.auth import auth_bp
    from api.execute import execute_bp
    from api.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(execute_bp, url_prefix='/api/execute')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'  # Ensure this path is correct
    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Compiler as a Service API"
        }
    )
    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    # Enable detailed error messages in development
    if config_name == 'development':
        @app.errorhandler(Exception)
        def handle_exception(e):
            import traceback
            traceback.print_exc()
            return jsonify(error=str(e)), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
