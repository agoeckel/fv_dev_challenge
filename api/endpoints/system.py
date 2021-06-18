import shutil
import io
import base64

from flask_restplus import Resource, Namespace, fields
from flask import jsonify, make_response, g
from flask import request, Response
from flask import stream_with_context, send_file
import uuid
import json
import re
import subprocess
from subprocess import PIPE, STDOUT
import http.client

from pathlib import Path

import datetime
import os
import time
import requests
import math
import settings
import string

ns = Namespace('system', description='System Management')

def check_connection():
    try:
        #CREATE TERMINAL COMMAND TO CHECK ONLINE CONNECTION
        return False
    except subprocess.TimeoutExpired:
        return False

@ns.route('/online_status')
class OnlineStatus(Resource):
    def get(self):
        return check_connection()

#CREATE AN ENDPOINT THAT RETURNS AN ARRAY OF ALL EVEN NUMBERS BETWEEN
#A RANGE OF TWO PASSED URL PARAMETERS
#HANDLE ERRORS AND EDGE CASES