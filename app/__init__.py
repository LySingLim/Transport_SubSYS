from flask import Flask
from .routes import register_routes
import time
import os

def create_app():
    # Set up Flask application
    static_folder = os.path.abspath('./static')
    template_folder = os.path.abspath('./templates')

    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable static file caching
    # Ensure templates auto-reload in development
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    register_routes(app)

    @app.after_request
    def add_header(response):
        # Disable caching for all requests
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.context_processor
    def inject_time():
        return {'time': time}

    return app
