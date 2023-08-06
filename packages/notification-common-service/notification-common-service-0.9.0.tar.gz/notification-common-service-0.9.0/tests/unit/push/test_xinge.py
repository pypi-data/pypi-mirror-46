# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from unittest import TestCase

import mock
from faker import Faker

from notification_service.push.base import ClientSystem, ServiceProvider, Environment
from notification_service.push.xinge import XingeMessage, XingeSender
from tests.unit.push import TestMessage, create_Message

faker = Faker()


def create_XingeMessage(**kwargs):
    return create_Message(XingeMessage, **kwargs)


class test_XingeMessage(TestMessage):

    def test_android(self):
        msg = create_XingeMessage(
            client_type='xinge-android', title=self.title, content=self.content)
        assert msg.client_system == ClientSystem.Android
        assert msg.service_provider == ServiceProvider.xinge

    def test_android_custom_msg(self):
        msg = create_XingeMessage(
            client_type='xinge-android', title=self.title, content=self.content,
            custom_msg={
                'title': self.new_title,
                'content': self.new_content,
            })
        msg_object = msg.to_msg_object()
        assert msg_object.raw['title'] == self.new_title
        assert msg_object.raw['content'] == self.new_content

    def test_ios(self):
        msg = create_XingeMessage(client_type='xinge-ios', title=self.title,
                                  content=self.content, environment=Environment.production)
        assert msg.client_system == ClientSystem.iOS
        assert msg.service_provider == ServiceProvider.xinge

    def test_ios_custom_msg(self):
        environment = Environment.production
        msg = create_XingeMessage(client_type='xinge-ios', title=self.title,
                                  content=self.content, environment=environment,
                                  custom_msg={
                                      'aps': {
                                          'alert': {
                                              'title': self.new_title,
                                              'body': self.new_content,
                                          }
                                      }
                                  })
        msg_object = msg.to_msg_object()
        assert msg_object.raw['aps']['alert']['title'] == self.new_title
        assert msg_object.raw['aps']['alert']['body'] == self.new_content


class test_XingeSender(TestCase):

    def setUp(self):
        self.access_id = '2200321268'
        self.secret_key = '2a020ed64ef2e31e352f076d7460543a'
        self.target = 'bc648aa880d4757127a4433ddda073b19f8454a60bd53b6da952890ca11848cf'
        self.client_types = ['xinge-ios', 'xinge-android']

        # self.mock_PushSingleDevice_success = mock.Mock(return_value=(0, ''))
        self.mock_QueryDeviceCount_success = mock.Mock(return_value=(0, 12))

    def test_sender(self):
        for client_type in self.client_types:
            msg = create_XingeMessage(client_type=client_type)
            sender = XingeSender(
                access_id=self.access_id, secret_key=self.secret_key,
                client_type=client_type, environment=Environment.development)
            # sender._client.PushSingleDevice = self.mock_PushSingleDevice_success
            assert sender.push_single_device(msg, self.target).is_success

    def test_check_authorization(self):
        for clien_type in self.client_types:
            sender = XingeSender(
                access_id=self.access_id, secret_key=self.secret_key,
                client_type=clien_type)
            assert sender.check_authorization().is_success
