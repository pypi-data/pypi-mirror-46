# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class StateBase(object):
    """Base class of states."""
    detail = ''

    def __init__(self, detail=''):
        self.detail = str(detail)

    @property
    def is_success(self):
        return isinstance(self, Success)

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return 'State name: {name}. Detail: {detail}.'\
            .format(name=self.name, detail=self.detail)

    def __unicode__(self):
        return unicode(self.__str__())


class PushState(StateBase):
    """Push state."""


class Success(StateBase):
    """Success."""


class UnknowPushState(PushState):
    pass


class PushExcetion(PushState):

    def __init__(self, exception, detail=''):
        detail += '{}: {}'.format(exception.__class__.__name__, str(exception))
        super(PushExcetion, self).__init__(detail=detail)


class CheckAuthorizationExcetion(PushExcetion):
    pass
