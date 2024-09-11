#!/usr/bin/env python3
"""Auth Module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password function"""

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
