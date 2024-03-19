from flask import Flask
from flask_cors import CORS
from config import Config

from .routes.usuario_bp import usuario_bp
from .routes.servidor_bp import servidor_bp
from .routes.canal_bp import canal_bp
from .routes.mensaje_bp import mensaje_bp
from .routes.error_handlers import errors
from .routes.rol_bp import rol_bp
from .routes.status_bp import status_bp

from .database import DatabaseConnection
import os
from flask import flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def init_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_object(
        Config
    )
    

    DatabaseConnection.set_config(app.config)
    
   
    CORS(app,  origins="http://127.0.0.1:5500", supports_credentials=True, allow_headers=["Content-Type", "Authorization"]
 
    )
    

   

    app.register_blueprint(usuario_bp, url_prefix = '/usuario')
    app.register_blueprint(status_bp, url_prefix = '/status')
    app.register_blueprint(rol_bp, url_prefix = '/rol')
    app.register_blueprint(servidor_bp, url_prefix = '/servidor')
    app.register_blueprint(canal_bp, url_prefix = '/canal')
    app.register_blueprint(mensaje_bp, url_prefix = '/mensaje')
    app.register_blueprint(errors)
    return app
    