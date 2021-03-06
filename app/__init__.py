from flask import Flask
from config import Config

def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    
    with flask_app.app_context():
        from app.dashboard import init_dashboard
        dash_app = init_dashboard(flask_app)

    return dash_app