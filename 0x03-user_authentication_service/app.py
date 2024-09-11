#!/usr/bin/env python3
"""Flask app Module"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """Default route for flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """post to users function"""
    q = dict(request.form)
    try:
        user = AUTH.register_user(q["email"], q["password"])
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": user.email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """post sessions function"""
    q = dict(request.form)
    if not AUTH.valid_login(q["email"], q["password"]):
        abort(401)
    session_id = AUTH.create_session(q["email"])
    response = jsonify({"email": q["email"], "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
