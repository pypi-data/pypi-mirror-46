# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class PushError(Exception):
    pass


class ClientTypeError(PushError, ValueError):
    """Client Type infomation error"""


class CidTypeError(PushError, ValueError):
    """cid type error"""


class SenderError(PushError):
    pass


class AWSSenderError(SenderError):
    pass


class RequireFieldsError(Exception):

    need_fields = set()

    def __init__(self, fields):
        self.need_fields = fields

    def __str__(self):
        return 'Fields {} is need.'.format(tuple(self.need_fields))
