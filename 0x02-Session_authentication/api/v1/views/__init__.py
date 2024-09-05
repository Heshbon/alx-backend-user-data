#!/usr/bin/env python3
""" Defines the blueprint for the API"""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import session_auth  # Imports session_auth view

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

app_views.register_blueprint(session_auth)  # Registers session_auth blueprint

User.load_from_file()
