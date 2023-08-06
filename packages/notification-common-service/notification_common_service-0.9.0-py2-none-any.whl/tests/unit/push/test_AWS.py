# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from unittest import TestCase

import mock
from faker import Faker

from notification_service.push.AWS import AWSMessage, AWSSender, AWSiOSContentKey
from notification_service.push.base import ClientSystem, ServiceProvider, Environment
from tests.unit.push import TestMessage, create_Message

faker = Faker()


def create_AWSMessage(**kwargs):
    return create_Message(AWSMessage, **kwargs)


class test_AWSMessage(TestMessage):

    def test_android(self):
        msg = create_AWSMessage(client_type='aws-android',
                                title=self.title, content=self.content)
        assert msg.client_system == ClientSystem.Android
        assert msg.service_provider == ServiceProvider.AWS

    def test_android_custom_msg(self):
        msg = create_AWSMessage(client_type='aws-android',
                                title=self.title, content=self.content, custom_msg={
                'GCM': {
                    'data': {
                        'title': self.new_title,
                        'message': self.new_content,
                    }
                }
            })
        data = msg.to_msg_object()
        assert json.loads(data['GCM'])['data']['title'] == self.new_title
        assert json.loads(data['GCM'])['data']['message'] == self.new_content

    def test_ios(self):
        msg = create_AWSMessage(client_type='aws-ios', title=self.title,
                                content=self.content,
                                environment=Environment.production)
        assert msg.client_system == ClientSystem.iOS
        assert msg.service_provider == ServiceProvider.AWS

    def test_ios_custom_msg(self):
        environment = Environment.production
        ios_content_key = AWSiOSContentKey.__members__[environment.value].value
        msg = create_AWSMessage(client_type='aws-ios', title=self.title,
                                content=self.content,
                                environment=environment, custom_msg={
                ios_content_key: {
                    'aps': {
                        'alertTitle': self.new_title,
                        'alert': self.new_content,
                    }
                }
            })
        data = msg.to_msg_object()
        assert json.loads(data[ios_content_key])[
                   'aps']['alertTitle'] == self.new_title
        assert json.loads(data[ios_content_key])[
                   'aps']['alert'] == self.new_content


class test_AWSSender(TestCase):

    def setUp(self):
        self.target = 'arn:aws:sns:us-east-1:108935729014:endpoint/GCM/D3_test\
            /ec332e06-06d4-3457-b2fc-68c8f543aa14'
        self.application_arn = 'arn:aws:sns:us-east-1:108935729014:app/GCM/D3_test'
        self.region_name = 'us-east-1'
        self.access_id = 'AKIAJ5NDSRIBIZ6O5VEQ'
        self.secret_key = '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'
        self.mock_publish_success = mock.Mock(return_value={'ResponseMetadata': {
            'RetryAttempts': 0, 'HTTPStatusCode': 200,
            'RequestId': '50d68dd3-5b5f-5db7-b4c3-d95ebcc3438e',
            'HTTPHeaders': {'x-amzn-requestid': '50d68dd3-5b5f-5db7-b4c3-d95ebcc3438e',
                            'date': 'Fri, 14 Dec 2018 17:16:12 GMT',
                            'content-length': '294',
                            'content-type': 'text/xml'}},
            u'MessageId': 'c4c1c592-7bfe-5c1c-bda6-911f9c627225'})
        self.client_types = ['aws-ios', 'aws-android']

    def test_sender_with_application_arn(self):
        for client_type in self.client_types:
            self._test_sender_with_application_arn(client_type)

    def test_sender_with_region_name(self):
        for client_type in self.client_types:
            self._test_sender_with_region_name(client_type)

    def _test_sender_with_application_arn(self, client_type):
        msg = create_AWSMessage(client_type=client_type)
        sender = AWSSender(access_id=self.access_id, secret_key=self.secret_key,
                           application_arn=self.application_arn,
                           client_type=client_type)
        assert sender.region_name != ''

        sender._client.publish = self.mock_publish_success
        assert sender.push_single_device(msg, self.target).is_success

    def _test_sender_with_region_name(self, client_type):
        msg = create_AWSMessage(client_type=client_type)
        sender = AWSSender(access_id=self.access_id, secret_key=self.secret_key,
                           region_name=self.region_name, client_type=client_type)
        assert sender.region_name != ''

        sender._client.publish = self.mock_publish_success
        assert sender.push_single_device(msg, self.target).is_success

    def test_check_authorization(self):
        for client_type in self.client_types:
            sender = AWSSender(access_id=self.access_id, secret_key=self.secret_key,
                               application_arn=self.application_arn,
                               client_type=client_type)
            assert sender.check_authorization().is_success

    def test_create_platform_endpoint(self):
        for client_type in self.client_types:
            sender = AWSSender(access_id=self.access_id, secret_key=self.secret_key,
                               application_arn=self.application_arn,
                               client_type=client_type)
            token = 'c7ef3cb5e31a40a084672d55f46cfd964b9b32ddf62d3b4b0609c4a52837aa41'
            result = sender.create_platform_endpoint(token)
            assert result.is_success
