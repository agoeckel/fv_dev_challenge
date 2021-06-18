import os
import uuid
import json

from pathlib import Path
import datetime

from flask import Flask, Blueprint
from flask import render_template, send_from_directory
from flask import session, jsonify, make_response, g
from flask import request, Response

from api.endpoints.system import ns as system_ns
from flask_restplus import Api
from flask_cors import CORS
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token,
#     get_jwt_identity
# )

import settings

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    app.config['JWT_SECRET_KEY'] = 'imagerie'
    
    app.secret_key = 'any random string'
    blueprint = Blueprint('api', __name__, url_prefix='/api/capture')
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }

    settings.api = Api(blueprint,version='1.0', title='FV sAPI',
            description='Testing api',security='Bearer Auth', authorizations=authorizations)
    settings.api.add_namespace(system_ns)

    CORS(app, resources=r'/api/*', allow_headers='*')
    app.register_blueprint(blueprint)

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    return app
