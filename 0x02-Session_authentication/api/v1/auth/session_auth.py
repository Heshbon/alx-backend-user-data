#!/usr/bin/env python3
""" The module function for session suthentication"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ The session class authentication to manage user sessions"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a session ID for a given user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            The session ID if user_id is valid, otherwise None."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves a user ID based on a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            The user ID if session_id is valid, otherwise Non"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """ Retrieves the user associated with the request."""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)
