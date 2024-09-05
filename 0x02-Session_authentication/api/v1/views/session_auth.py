#!/usr/bin/env python3

""" The module function that defines routes for session authentication."""
import os

from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User as DBUser
from typing import Union
from flask import session


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """ Logs a user and set the session cookie."""
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        user: DBUser = DBUser.search({"email": email})[0]
    except IndexError:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    data = jsonify(user.to_json())
    data.set_cookie(os.environ.get("SESSION_NAME"), session_id)

    return data
