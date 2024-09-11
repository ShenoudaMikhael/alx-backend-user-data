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

    @classmethod
    def register_user(self, email: str, password: str) -> User:
        """register user function"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, str(hashed_password))
        return None
