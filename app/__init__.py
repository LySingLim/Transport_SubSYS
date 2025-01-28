from flask import Flask
from .routes import register_routes
import time
import os  # Import the os module

def create_app():
    # Resolve the absolute path for static and template folders
    static_folder = os.path.abspath('./static')
    template_folder = os.path.abspath('./templates')

    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

    # Disable static file caching in development
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    register_routes(app)

    @app.context_processor
    def inject_time():
        return {'time': time}

    return app
