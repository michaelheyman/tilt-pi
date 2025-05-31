"""Tilt Pi error classes."""

class TiltPiError(Exception):
    """Base exception for Tilt Pi."""


class TiltPiConnectionError(TiltPiError):
    """Error occurred while communicating with Tilt Pi."""


class TiltPiConnectionTimeoutError(TiltPiConnectionError):
    """Timeout occurred while communicating with Tilt Pi."""
