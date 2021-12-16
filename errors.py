# -*- coding: utf-8 -*-


class NotFound(Exception):
    """Custom exception class to be thrown when local error occurs."""
    pass


class InsignificantError(Exception):
    """Custom exception class to be thrown when local error occurs."""

    def __init__(self, payload={}):
        self.payload = payload

    def __str__(self):
        return str(self.payload)


class BadRequest(Exception):
    """Custom exception class to be thrown when local error occurs."""

    def __init__(self, note, status=400, payload={}):
        self.note = note
        self.status = status
        self.payload = payload

    def __str__(self):
        return self.note


class BizError(Exception):
    """ Biz Error """

    def __init__(self, note, status=400, payload={}):
        self.note = note
        self.status = status
        self.payload = payload

    def __str__(self):
        return self.note


class DuplicateError(Exception):
    """ Duplicate Error """

    def __init__(self, note, status=400, payload={}):
        self.note = note
        self.status = status
        self.payload = payload

    def __str__(self):
        return self.note


class CriticalError(Exception):
    """ Critical Error """

    def __init__(self, note, status=500, payload={}):
        self.note = note
        self.status = status
        self.payload = payload

    def __str__(self):
        return self.note
