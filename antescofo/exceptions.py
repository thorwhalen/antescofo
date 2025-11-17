"""
Custom exceptions for the Antescofo Python interface.
"""


class AntescofoException(Exception):
    """Base exception for all Antescofo-related errors."""

    pass


class ConnectionError(AntescofoException):
    """Raised when connection to Antescofo fails."""

    pass


class OSCError(AntescofoException):
    """Raised when OSC communication fails."""

    pass


class ScoreError(AntescofoException):
    """Raised when score file operations fail."""

    pass


class TimeoutError(AntescofoException):
    """Raised when an operation times out."""

    pass


class InvalidMessageError(AntescofoException):
    """Raised when an invalid OSC message is received."""

    pass
