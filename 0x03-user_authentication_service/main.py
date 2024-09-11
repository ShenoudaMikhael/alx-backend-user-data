#!/usr/bin/env python3
"""Main Module"""

import requests

from app import AUTH

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test register user"""
    url = "{}/users".format(BASE_URL)
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=data)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test log in wrong password"""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    assert res.status_code == 401


def profile_unlogged() -> None:
    """test profile unlogged"""
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """test profile logged"""
    url = "{}/profile".format(BASE_URL)
    cookies = {"session_id": session_id}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    payload = res.json()
    assert "email" in payload
    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == payload["email"]


def log_out(session_id: str) -> None:
    """Test log out"""
    url = "{}/sessions".format(BASE_URL)
    headers = {"Content-Type": "application/json"}
    data = {"session_id": session_id}
    res = requests.delete(url, headers=headers, cookies=data)
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """test reset password token"""
    url = "{}/reset_password".format(BASE_URL)
    data = {"email": email}
    res = requests.post(url, data=data)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    reset_token = res.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password"""
    url = "{}/reset_password".format(BASE_URL)
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    res = requests.put(url, data=data)
    assert res.status_code == 200
    assert res.json()["message"] == "Password updated"
    assert res.json()["email"] == email


def log_in(email: str, password: str) -> str:
    """test log in"""
    url = "{}/sessions".format(BASE_URL)
    data = {"email": email, "password": password}
    res = requests.post(url, data=data)
    if res.status_code == 401:
        return "Invalid credentials"
    assert res.status_code == 200
    res_json = res.json()
    assert "email" in res_json
    assert "message" in res_json
    assert res_json["email"] == email
    return res.cookies.get("session_id")


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
