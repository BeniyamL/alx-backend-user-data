#!/usr/bin/env python3
"""
session authentication module
"""
from typing import Dict, TypeVar
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    a session authorization class
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create_session - funciton to create a session id for a user
        Arguments:
            user_id - the given user id
        Returns:
            the session id created for the given user id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        user_id_for_session_id - method to return the user id from session id
        Arguments:
            session_id - the given session id
        Returns:
            the user id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        current_user - method to return the current user based on cookie value
        Arguments:
            request: the given request
        Returns:
            the current user id
        """
        sesn_id: str = self.session_cookie(request)
        usr_id: str = self.user_id_for_session_id(sesn_id)
        current_usr: TypeVar('User') = User.get(usr_id)
        return current_usr

    def destroy_session(self, request=None):
        """
        destroy_session - method to destory the session
        Arguments:
            request: the given request
        Returns:
            true if it is successfully deleted false otherwise
        """
        if request is None:
            return False
        sesn_id: str = self.session_cookie(request)
        if sesn_id is None:
            return False
        usr_id: str = self.user_id_for_session_id(sesn_id)
        if usr_id is None:
            return False
        try:
            del self.user_id_by_session_id[sesn_id]
        except Exception:
            pass
        return True
