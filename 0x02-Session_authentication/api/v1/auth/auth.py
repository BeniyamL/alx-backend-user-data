#!/usr/bin/env python3
"""
a python module to create a basic authentication method
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    class for basic authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth - a function to check the autherization path
        Arguments:
            path: the given path
            excluded_paths: the path to be excluded
        Returns:
            True if the path is not in excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'

        for p in excluded_paths:
            if p.endswith('*'):
                pth = p[:-1]
                if path.startswith(pth):
                    return False
            else:
                if p[-1] != '/':
                    p += '/'
                if path == p:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header - a function to find the autherization header
        Arguments:
            request: the given request
        Returns:
            none if it does not contianer authorization key
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user - a function to return the current user
        """
        return None

    def session_cookie(self, request=None):
        """
        session_cookie - fucntion to return cookie value from request
        Arguments:
            request: the given request
        Returns:
            the cookie value
        """
        if request is None:
            return None
        env_session = getenv('SESSION_NAME', None)
        return request.cookies.get(env_session, None)
