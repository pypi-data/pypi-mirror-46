# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest

from notification_service.push.base import (ClientSystem, Environment,
                                            PushType, ServiceProvider)
from notification_service.push.jiguang import JiguangMessage, JiguangSender
from tests.unit.push import create_Message, faker


def create_JiguangMessage(**kwargs):
    return create_Message(JiguangMessage, **kwargs)


class TestJiguangMessage(object):

    @pytest.fixture(autouse=True)
    def setup_fake_content(self):
        self.title = faker.name()
        self.content = faker.text()
        self.new_title = faker.name()
        self.new_content = faker.text()

    def test_android(self):
        msg = create_JiguangMessage(
            client_type='jiguang-android', title=self.title, content=self.content)
        assert msg.client_system == ClientSystem.Android
        assert msg.service_provider == ServiceProvider.jiguang

    def test_android_custom_msg(self):
        msg = create_JiguangMessage(client_type='jiguang-android', title=self.title,
                                    content=self.content,
                                    custom_msg={
                                        'alert': self.new_content,
                                        'title': self.new_title,
                                        'category': 'test',
                                    })
        msg_object = msg.to_msg_object()
        assert msg_object['alert'] == self.new_content
        assert msg_object['title'] == self.new_title
        assert msg_object['category'] == 'test'

    def test_android_custom_msg_with_unsupport_custom_msg(self):
        msg = create_JiguangMessage(
            client_type='jiguang-android', title=self.title, content=self.content,
            custom_msg={
                'title': self.new_title,
                'content': self.new_content,
            })
        msg_object = msg.to_msg_object()
        assert msg_object['title'] == self.title
        assert msg_object['alert'] == self.content

    def test_ios(self):
        msg = create_JiguangMessage(client_type='jiguang-ios', title=self.title,
                                    content=self.content,
                                    environment=Environment.production)
        assert msg.client_system == ClientSystem.iOS
        assert msg.service_provider == ServiceProvider.jiguang
        msg_object = msg.to_msg_object()
        assert msg_object['alert']['title'] == self.title
        assert msg_object['alert']['body'] == self.content

    def test_ios_custom_msg(self):
        msg = create_JiguangMessage(client_type='jiguang-ios', title=self.title,
                                    content=self.content,
                                    environment=Environment.development,
                                    custom_msg={
                                        'alert': {
                                            'title': self.new_title,
                                            'body': self.new_content,
                                        },
                                        'badge': 12,
                                        'sound': 'car.caf',
                                        'extras': {
                                            'key1': 'value1',
                                            'key2': 'value2',
                                        }
                                    })
        msg_object = msg.to_msg_object()
        assert msg_object['alert']['title'] == self.new_title
        assert msg_object['alert']['body'] == self.new_content
        assert msg_object['badge'] == 12
        assert msg_object['sound'] == 'car.caf'
        assert msg_object['extras'] == {
            'key1': 'value1',
            'key2': 'value2',
        }


class TestJiguangSender(object):

    @pytest.fixture()
    def push_info_ios(self):
        self.access_id = 'fe838f2bd6a1c1f92f0f3e7f'
        self.secret_key = '71fcab6158485e8b330b3178'
        self.target = '121c83f76079ae8c516'


    @pytest.fixture()
    def push_info_android(self):
        self.access_id = '069fe15945e3be255d615f92'
        self.secret_key = 'b8239f74fb1b8b2029d7fb65'
        self.target = '18071adc034c033355a'

    def test_sender_iOS(self, push_info_ios):
        client_type = 'jiguang-ios'
        msg = create_JiguangMessage(client_type=client_type,
                                    push_type=PushType.notification,
                                    environment=Environment.development,
                                    custom_msg={
                                        'alert': {
                                            'title': 'title of jiguang',
                                            'body': 'content of jiguang',
                                        },
                                        'sound': 'car.caf',
                                        'extras': {
                                            'product_key': 'asdfasfdasd',
                                            'did': 'value2',
                                        }
                                    })
        sender = JiguangSender(
            access_id=self.access_id, secret_key=self.secret_key,
            client_type=client_type)
        assert sender.push_single_device(msg, self.target).is_success

    def test_sender_Android(self, push_info_android):
        client_type = 'jiguang-android'
        msg = create_JiguangMessage(client_type=client_type,
                                    push_type=PushType.notification,
                                    custom_msg={
                                        'alert': 'content of jiguang',
                                        'title': 'title of jiguang',
                                        'category': 'test',
                                    })
        sender = JiguangSender(
            access_id=self.access_id, secret_key=self.secret_key,
            client_type=client_type)
        assert sender.push_single_device(msg, self.target).is_success

    def test_check_authorization(self, push_info_ios):
        for clien_type in ['jiguang-ios', 'jiguang-android']:
            sender = JiguangSender(
                access_id=self.access_id, secret_key=self.secret_key,
                client_type=clien_type)
            assert sender.check_authorization().is_success
