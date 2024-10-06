import logging
from flask import Flask
from src.config import Config
from src.routes.process import process_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configure logging to output to stdout
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    # Register blueprints
    app.register_blueprint(process_bp)

    return app