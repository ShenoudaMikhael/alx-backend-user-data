#!/usr/bin/env python3
"""user session model"""

from .base import Base


class UserSession(Base):
    """User Session class"""

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self._password = kwargs.get("_password")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
