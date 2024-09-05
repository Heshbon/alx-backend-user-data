#!/usr/bin/env python3
""" The auth class function"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Authentication class."""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """ Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (list): A list of paths that do not require authent.

        Returns:
        True if the path requires authentication, False otherwise."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request."""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user."""
        return None

    def session_cookie(self, request=None):
        """ Return a cookie value from a request."""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None

        return request.cookies.get(session_name)
