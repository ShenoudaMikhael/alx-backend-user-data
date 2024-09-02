#!/usr/bin/env python3
"""Auth module"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth function"""
        if (
            path not in excluded_paths
            or path is None
            or "{}/".format(path) not in excluded_paths
        ):
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """authorization_header function"""
        return request

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user function"""
        return request if request else None
