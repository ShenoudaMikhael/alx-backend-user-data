#!/usr/bin/env python3
"""Hash password Module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password function"""
    return bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt())
