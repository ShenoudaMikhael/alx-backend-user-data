#!/usr/bin/env python3
""" Module of Session Auth """

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """login user function"""

    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"})
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"})

    users = User.search({"email": email})
    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"})
