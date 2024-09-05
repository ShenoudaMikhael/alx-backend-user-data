#!/usr/bin/env python3
"""Session Auth Module"""
from .auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """Session Auth Class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session function"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """user id for session id function"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar("User"):
        """current user function"""
        sesssion_key = self.session_cookie(request)
        if sesssion_key is None:
            return None
        user_id = self.user_id_for_session_id(sesssion_key)
        if user_id is None:
            return None
        user = User.get(user_id)
        if user is None:
            return None
        return user

    def destroy_session(self, request=None):
        """destroy session function"""
        if request is None:
            return False

        sc = self.session_cookie(request)
        if sc is None:
            return False
        uid = self.user_id_for_session_id(sc)
        if uid is None:
            return False
        del self.user_id_by_session_id[sc]
        return True
