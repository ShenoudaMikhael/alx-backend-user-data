#!/usr/bin/env python3
"""Auth Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user with email and paswword"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """valid login function"""
        try:
            user = self._db.find_user_by(email=email)
            result = bcrypt.checkpw(
                password.encode("utf-8"),
                user.hashed_password,
            )
            return result
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """create session function"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None


def _hash_password(password: str) -> bytes:
    """hash password function"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate uuid function"""
    return str(uuid.uuid4())
