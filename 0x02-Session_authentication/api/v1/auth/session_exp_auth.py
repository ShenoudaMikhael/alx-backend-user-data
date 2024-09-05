#!/usr/bin/env python3
"""Session exp auth module"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class"""

    def __init__(self):
        self.session_duration = int(getenv("SESSION_DURATION", "0"))

    def create_session(self, user_id=None):
        """create session function"""
        sid = super(user_id)
        if sid is None:
            return None
        self.user_id_by_session_id[sid] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }

    def user_id_for_session_id(self, session_id=None):
        """user id for session id function"""

        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if "created_at" not in session_dict:
            return None
        if session_dict["created_at"] + self.session_duration < datetime.now():
            return None
        return session_dict["user_id"]
