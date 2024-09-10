#!/usr/bin/env python3
""" The Auth function module"""
import bcrypt
import uuid

from typing import Optional
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hash a password using bcrypt and return the hashed password as bytes.

    Args:
        password (str): The password to hash.

    Returns:
    The salted hash of the input password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """ Auth class to interact with the authentication database."""
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user

        Args:
            email (str): The email of the user.
            password (str): The plaintext password for the new user.

        Returns:
        The newly created User object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password=password)
            new_user = self._db.add_user(
                    email=email, hashed_password=hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if the provided email and password are valid for login

        Args:
            email (str): The email of the user.
            password (str): The plaintext password provided by the user

        Returns:
        True if the login is valid, False otherwise."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    @staticmethod
    def _generate_uuid() -> str:
        """ Generate a unique identifier (UUID) for session management

        Returns:
        The string representatin of the generated UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """ Create a new session for the user identified by the given email.

        Args:
            email (str): The email of the user.

        Returns:
        The generated session ID if the user is found, or None if the user
        does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Retrieve a user session ID

        Args:
            session_id (str): The session ID.

        Returns:
        The corresponding User object, or None if no user is found."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy the session for the user with the specified user ID
        Args:
            user_id (int): The ID of the user.

        Returns:
        None"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generate a reset token for the user identified by the given email
        Args:
            email (str): The email of the user to generate the reset token.

        Returns:
            The generated reset token."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User does not exist")

        reset_token = str(uuid.uuid4())

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update the user's password using a reset token

        Args:
            reset_token (str): The reset token.
            password (str): The new password."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)

        self._db.update_user(
                user.id, hashed_password=hashed_password, reset_token=None)
