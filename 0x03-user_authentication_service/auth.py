#!/usr/bin/env python3
"""Hash password Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password function"""
    password = bcrypt.hashpw(
        password.encode(encoding="utf-8"), bcrypt.gensalt())
    return password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()
