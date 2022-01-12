#!/usr/bin/env python3
"""
session expirey module
"""
from typing import Dict
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    a class for session expiry module
    """
    def __init__(self) -> None:
        """
        overide the parent init method
        """
        sesn_dur = getenv('SESSION_DURATION', 0)
        try:
            sesn_dur = int(sesn_dur)
        except Exception:
            sesn_dur = 0
        self.session_duration = sesn_dur

    def create_session(self, user_id=None):
        """
        a method to overide the parent create session
        Arguments:
            user_id: the given user id
        Returns:
            the given the session id
        """
        sesn_id = super().create_session(user_id)
        if sesn_id is None:
            return None
        sesn_dict: Dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[sesn_id] = sesn_dict
        return sesn_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id_for_session_id - function to find user id by session id
        Arguments:
            session_id: the given session id
        Returns:
            the user id
        """
        if session_id is None or\
                session_id not in self.user_id_by_session_id.keys():
            return None

        sesn_dict: Dict = self.user_id_by_session_id.get(session_id)
        if sesn_dict is None or 'created_at' not in sesn_dict:
            return None
        usr_id = sesn_dict.get('user_id')
        if self.session_duration <= 0:
            return usr_id
        c_t = sesn_dict.get('created_at')
        if c_t is None:
            return None
        expire = c_t + timedelta(seconds=self.session_duration)
        if expire < datetime.now():
            return None
        return usr_id
