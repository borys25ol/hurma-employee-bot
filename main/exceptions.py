"""
Module for custom exceptions.
"""
CSRF_TOKEN_NOT_FOUND = "CSRF token not found."


class CsrfTokenNotFoundException(Exception):
    """
    CSRF token not found exception.
    """

    def __init__(self, message: str):
        self.message = message
