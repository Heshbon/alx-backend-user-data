#!/usr/bin/env python3
""" Implement a hash_password function"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Checks the password against a hashed password using bcrypt."""
    return bcrypt.checkpw(password.encode(), hashed_password)
