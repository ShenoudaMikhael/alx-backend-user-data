#!/usr/bin/env python3
"""Auth module"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth function"""
        if (
            path is None
            or excluded_paths is None
            or excluded_paths == []
            or (path not in excluded_paths
                and "{}/".format(path) not in excluded_paths)
        ):
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        if request is None:
            return None
        if request.headers.has_key("Authorization"):
            return request.headers["Authorization"]
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user function"""
        return None
