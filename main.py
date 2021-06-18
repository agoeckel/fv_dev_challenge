import os
import uuid
import json

from pathlib import Path
import datetime
import settings

from flask import Flask, Blueprint
from flask import render_template, send_from_directory
from flask import session, jsonify, make_response, g
from flask import request, Response
from api.endpoints.system import ns as system_ns

from flask_restplus import Api
from flask_cors import CORS
app = Flask(__name__,instance_relative_config=True)

app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
app.config['JWT_SECRET_KEY'] = 'imagerie'

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_TOKEN_LOCATION'] = ['headers','query_string']
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'any random string'

blueprint = Blueprint('api', __name__, url_prefix='/api')
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}
settings.api = Api(blueprint,version='1.0', title='FV API',
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


if __name__ == '__main__':
    PORT = int(os.getenv('PORT')) if os.getenv('PORT') else 5025

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host='0.0.0.0', port=PORT, debug=True)