#!/usr/bin/env python3
"""Session exp auth module"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Exp Auth class"""

    def __init__(self):
        sd = getenv("SESSION_DURATION")

        try:
            session_duration = int(sd)
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """create session function"""
        if user_id is None:
            return None
        sid = super().create_session(user_id)

        if sid is None:
            return None
        self.user_id_by_session_id[sid] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        return sid

    def user_id_for_session_id(self, session_id=None):
        """user id for session id function"""

        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        td = created_at + timedelta(seconds=self.session_duration)
        if td < datetime.utcnow():
            return None
        return session_dict.get("user_id")
