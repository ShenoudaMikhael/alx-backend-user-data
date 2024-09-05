#!/usr/bin/env python3
""" Module of Session Auth """

from api.v1.views import app_views
from flask import request, jsonify, session
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """login user function
    check user email and password
    """

    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            from api.v1.app import auth

            sid = auth.create_session(user.id)
            ss = getenv("SESSION_NAME")
            response = jsonify(user.to_json())
            response.set_cookie(ss, sid)

            return response
    return jsonify({"error": "wrong password"}), 401
