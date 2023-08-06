# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


from .states import Success


class ResultBase(object):
    """Base class for results."""
    state = None
    data = None

    def __init__(self, state=Success(), data=None):
        self.state = state
        if data:
            self.data = data

    @property
    def is_success(self):
        return self.state.is_success

    def __unicode__(self):
        return self.state.__unicode__()

    def __str__(self):
        return self.state.__str__()


class PushResult(ResultBase):
    """App push state."""
