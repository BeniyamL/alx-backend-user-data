#!/usr/bin/env python3
"""
an authorization module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(psswrd: str) -> bytes:
    """
    _hass_password - method to return the hasshed password
    Arguments:
        psswrd: the given password
    Returns:
        the hassed password
    """
    hsh_psswrd = bcrypt.hashpw(
                                psswrd.encode('utf-8'),
                                bcrypt.gensalt(prefix=b"2b")
                                )
    return str(hsh_psswrd.decode())


def _generate_uuid() -> str:
    """
    _generate_uuid - function to generate a unique id using uuid
    Arguments:
        nothing
    Returns:
        the string representation of a new uuid
    """
    new_id = str(uuid4())
    return new_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user - method to register a givn user
        Arguments:
            email: the given email
            password: the given password
        Returns:
            the created user
        """
        try:
            user_exist = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hsd_psswrd: str = _hash_password(password)
            new_usr = self._db.add_user(email, hsd_psswrd)
            return new_usr

    def valid_login(self, email: str, password: str) -> bool:
        """
        valid_login - method to validate a login page
        Arguments:
            email: the given email
            password: the given password
        Returns:
            true if the user is valid false if it is not valid
        """
        try:
            user_exist = self._db.find_user_by(email=email)
            if bcrypt.checkpw(
                                password.encode('utf-8'),
                                str.encode(user_exist.hashed_password)
                            ):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        create_session - method to create a session id
        Arguments:
            email: the given email
        Returns:
            the session id
        """
        try:
            user_exist = self._db.find_user_by(email=email)
            sesn_id = _generate_uuid()
            self._db.update_user(user_exist.id, session_id=sesn_id)
            return sesn_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        get_user_from_session_id - fucntion to find user from the session
        Arguments:
            session_id: the given session id
        Returns:
            the user id corresponance to the given session id
        """
        if session_id is None:
            return None
        try:
            usr_exist = self._db.find_user_by(session_id=session_id)
            return usr_exist
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """
        a method to destroy the session based
        Arguments:
            user_id: the given user id
        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except (KeyError, ValueError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        get_reset_password_token - function to to generate new uuid
        Arguments:
            email: the given email
        Returns:
            the new token
        """
        if email is None:
            return None
        try:
            usr_exists = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(usr_exists.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update_password - function to update the password
        Arguments:
            reset_token: the given token
            password: the given password
        Returns:
            None
        """
        if reset_token is None or password is None:
            return None
        try:
            usr_exist = self._db.find_user_by(reset_token=reset_token)
            hash_psswrd: str = _hash_password(password)
            self._db.update_user(
                                usr_exist.id,
                                hashed_password=hash_psswrd,
                                reset_token=None
                                )
            return None
        except NoResultFound:
            raise ValueError
