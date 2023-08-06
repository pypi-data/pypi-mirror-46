# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json

import boto3
from enum import Enum

from notification_service.exceptions import (ClientTypeError, AWSSenderError)
from notification_service.result import PushResult
from notification_service.states import (
    UnknowPushState, PushExcetion, CheckAuthorizationExcetion, Success)
from notification_service.utils import from_ARN_to_region_name, update_sub_dict
from .base import (Sender, Message, ClientSystem,
                   ServiceProvider, PushType)


class AWSiOSContentKey(Enum):
    development = 'APNS_SANDBOX'
    production = 'APNS'


class AWSMessage(Message):
    _iOS_content_key = None

    def to_msg_object(self):
        if self.client_system is ClientSystem.iOS:
            return self._to_msg_object_iOS()
        if self.client_system is ClientSystem.Android:
            return self._to_msg_object_GCM()

    def _to_msg_object_GCM(self):
        data = {
            'GCM': {
                'notification': {
                    'title': self.title,
                    'body': self.content,
                    'sound': 'default',
                },
                'data': {
                    'system': 'android',
                }
            }
        }
        return self._encode_msg_content(
            self._apply_push_type(self._apply_custom_msg(data)),
            'GCM'
        )

    def _to_msg_object_iOS(self):
        data = {
            self._iOS_content_key: {
                'aps': {
                    'alert': {
                        'title': self.title,
                        'body': self.content,
                    },
                    'sound': 'default',
                }
            }
        }
        return self._encode_msg_content(
            self._apply_push_type(self._apply_custom_msg(data)),
            self._iOS_content_key
        )

    def _apply_custom_msg(self, data):
        if self.custom_msg:
            return update_sub_dict(data, self.custom_msg)
        return data

    def _apply_push_type(self, data):
        if self.push_type is PushType.custom_message:
            if self.client_system is ClientSystem.iOS:
                return self._apply_push_type_iOS(data)
            if self.client_system is ClientSystem.Android:
                return self._apply_push_type_GCM(data)
        return data

    def _apply_push_type_iOS(self, data):
        if self.push_type is PushType.custom_message:
            data[self._iOS_content_key]['aps']['content-available'] = 1
            data[self._iOS_content_key]['aps'].pop('alert', None)
            data[self._iOS_content_key]['aps'].pop('sound', None)
        return data

    def _apply_push_type_GCM(self, data):
        if self.push_type is PushType.custom_message:
            data['GCM'].pop('notification', None)
        return data

    def _encode_msg_content(self, data, key):
        data[key] = json.dumps(data[key])
        return data

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        self._environment = value
        self._iOS_content_key = AWSiOSContentKey.__members__[
            self.environment.value].value


class AWSSender(Sender):
    region_name = ''
    message_structure = 'json'
    _client = None
    application_arn = ''

    def __init__(self, *args, **kwargs):
        """init

        Arguments:
            access_id {str} -- Access key ID
            secret_key {str} -- Secret access key
            application_arn {str} -- Application ARN
            region_name {str} -- Region name of ARN
        """
        super(AWSSender, self).__init__(*args, **kwargs)

    def _init_config(self):
        super(AWSSender, self)._init_config()
        if self.application_arn:
            self.region_name = from_ARN_to_region_name(self.application_arn)
        self._client = boto3.client('sns',
                                    aws_access_key_id=self.access_id,
                                    aws_secret_access_key=self.secret_key,
                                    region_name=self.region_name)

    def _verify_info(self):
        super(AWSSender, self)._verify_info()
        if self.service_provider != ServiceProvider.AWS:
            raise ClientTypeError(
                'service provider `{}` is not `AWS`'.format(self.service_provider))
        if self.region_name == '':
            raise AWSSenderError('`region_name` should not be empty.')

    def check_authorization(self):
        try:
            response = self._client.get_platform_application_attributes(
                PlatformApplicationArn=self.application_arn)
        except Exception, e:
            return PushResult(CheckAuthorizationExcetion(e))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return PushResult(UnknowPushState(response))
        else:
            return PushResult(Success(response))

    def create_platform_endpoint(self, token):
        try:
            response = self._client.create_platform_endpoint(
                PlatformApplicationArn=self.application_arn, Token=token)
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return PushResult(UnknowPushState(response))
        else:
            return PushResult(Success(response), data=response['EndpointArn'])

    def push_single_device(self, msg, target):
        try:
            response = self._client.publish(
                TargetArn=target, MessageStructure='json',
                Message=json.dumps(msg.to_msg_object()))
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return PushResult(UnknowPushState(response))
        else:
            return PushResult(Success(response))
