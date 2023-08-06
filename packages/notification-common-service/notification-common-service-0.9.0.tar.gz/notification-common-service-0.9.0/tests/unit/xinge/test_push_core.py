# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from notification_service.xinge import push_core


class TestXingePush(object):

    def test_android(self, xinge_info, faker):
        resp = push_core.push_single_device(
            accessId=unicode(xinge_info['android']['access_id']),
            secretKey=unicode(xinge_info['android']['secret_key']),
            token=unicode(xinge_info['android']['target']),
            client_type='xinge-android',
            content=unicode('content'),
            title=unicode('title'),
            environment=0,
        )
        assert resp[0] == 0
        assert resp[2] is not None

    def test_ios(self, xinge_info, faker):
        resp = push_core.push_single_device(
            accessId=unicode(xinge_info['ios']['access_id']),
            secretKey=unicode(xinge_info['ios']['secret_key']),
            token=unicode(xinge_info['ios']['target']),
            client_type='xinge-ios',
            content=unicode('content'),
            title=unicode('title'),
            environment=1,
        )
        assert resp[0] == 0
        assert resp[2] is not None
