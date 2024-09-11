#!/usr/bin/env python3
"""Hash password Module"""
import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash password function"""
    return bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user function"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already0 exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
