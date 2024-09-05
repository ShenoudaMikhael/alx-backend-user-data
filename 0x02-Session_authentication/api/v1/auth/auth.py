#!/usr/bin/env python3
"""Auth Module"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""

        if (
            path is None
            or excluded_paths is None
            or excluded_paths == []
            or (
                path not in excluded_paths
                and "{}/".format(path) not in excluded_paths
                and len(
                    [
                        True
                        for e in excluded_paths
                        if e.endswith("*") and path.startswith(e[:-1])
                    ]
                )
                == 0
            )
        ):
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """current user function"""
        return None

    def session_cookie(self, request=None):
        """session cookie function"""
        if request is None:
            return None
        session_name = getenv("SESSION_NAME")

        if session_name is None:
            return None
        sid = request.cookies.get(session_name)

        return sid
