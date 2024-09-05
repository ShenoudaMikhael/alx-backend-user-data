#!/usr/bin/env python3
"""session db auth module"""
from datetime import timedelta, datetime
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth Class"""

    def create_session(self, user_id=None):
        """create session function"""
        if user_id is None:
            return None
        sid = super().create_session(user_id)
        if sid is None:
            return None
        kw = {"user_id": user_id, "session_id": sid}
        us = UserSession(**kw)
        us.save()
        UserSession.save_to_file()
        return sid

    def user_id_for_session_id(self, session_id=None):
        """user id for session id function"""
        if session_id is None:
            return None
        us = UserSession.search({"session_id": session_id})
        if not us:
            return None
        us = us[0]

        return us.user_id

    def destroy_session(self, request=None):
        """destroy function"""
        if request is None:
            return False
        sid = self.session_cookie(request)
        if not sid:
            return False
        us = UserSession.search({"session_id": sid})
        if us:
            us[0].remove()
            return True
        return False
