#!/usr/bin/env python3
"""
a python module for encryption
"""
import bcrypt


def hash_password(passwrd: str) -> bytes:
    """
    hash_password - function to encrypt the password
    Arguments:
        passwrd: the given password in plain text
    Returns:
        the encrypted password
    """
    pass_hashed = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid - fucntion to valide the plain password with the hash one
    Arguments:
        hashed_password: the given hassed password
        password: the plain password tex
    Returns:
        true if it matches false otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
