#!/usr/bin/env python3
"""Basic auth module"""
import base64
from typing import TypeVar
from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """Basic auth class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract base64 authorization header function"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            a = base64_authorization_header.encode("utf-8")
            bs = base64.b64decode(a)
            de = bs.decode('utf-8')
            return de
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract user credentials function"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        a = decoded_base64_authorization_header.split(":")

        if len(a) < 2:
            return None, None
        z = (a[0], ":".join(a[1:]))

        return z

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials function"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
        except Exception:
            return None

        for u in user:
            if u.is_valid_password(user_pwd):
                return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user function"""
        ah = self.authorization_header(request)
        if ah is None:
            return None
        ex = self.extract_base64_authorization_header(ah)
        if ex is None:
            return None
        de = self.decode_base64_authorization_header(ex)
        if de is None:
            return None
        us, pwd = self.extract_user_credentials(de)
        if us is None or pwd is None:
            return None
        user = self.user_object_from_credentials(us, pwd)
        if user is None:
            return None
        return user
