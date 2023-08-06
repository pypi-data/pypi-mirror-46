# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

import jpush
from enum import Enum

from notification_service.push.base import (Sender, Message, ClientSystem,
                                            ServiceProvider, PushType, Environment)
from notification_service.exceptions import ClientTypeError, SenderError, CidTypeError
from notification_service.result import PushResult
from notification_service.states import (
    UnknowPushState, PushExcetion, Success)
from notification_service.utils import update_sub_dict

logger = logging.getLogger(__name__)


class CidType(Enum):
    alias = 1
    registration_id = 2


class JiguangMessage(Message):

    def _to_msg_object_iOS(self):
        msg = {
            'alert': {
                'title': self.title,
                'body': self.content,
            }
        }
        msg = self._apply_push_type(self._apply_custom_msg(msg))
        try:
            return jpush.ios(**msg)
        except Exception, e:
            logger.warning(
                'jiguang iOS push apply custom_msg failure. error msg: {}'.format(e))
            return jpush.android(self.content, self.title)

    def _to_msg_object_android(self):
        msg = {
            'alert': self.content,
            'title': self.title,
        }
        msg = self._apply_push_type(self._apply_custom_msg(msg))
        try:
            return jpush.android(**msg)
        except Exception, e:
            logger.warning(
                'jiguang android push apply custom_msg failure. error msg: {}'.format(
                    e))
            return jpush.android(self.content, self.title)

    def _apply_custom_msg(self, msg):
        if self.custom_msg:
            msg = update_sub_dict(msg, self.custom_msg)
        return msg

    def _apply_push_type(self, msg):
        """极光 push type 的区分在推送阶段，请查看 Sender 的推送方法 `push_single_device`"""
        return msg


class JiguangSender(Sender):

    def _init_config(self):
        super(JiguangSender, self)._init_config()
        self._clent = jpush.JPush(self.access_id, self.secret_key)

    def _verify_info(self):
        super(JiguangSender, self)._verify_info()
        if self.service_provider != ServiceProvider.jiguang:
            raise ClientTypeError(
                'service provider `{}` is not `jiguang`'.format(self.service_provider))

    def check_authorization(self):
        push = self._clent.create_push()
        push.message = jpush.message('')
        push.platform = jpush.all_
        push.audience = jpush.all_
        try:
            response = push.send_validate()
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response.status_code != 200:
            return PushResult(UnknowPushState(response.payload))
        else:
            return PushResult(Success(response.payload))

    def push_single_device(self, msg, target, cid_type=CidType.registration_id):
        if not isinstance(cid_type, CidType):
            raise CidTypeError('`cid_type` should be a `CidType` type value, not `{}`'
                               .format(type(cid_type)))
        push = self._clent.create_push()
        if cid_type == CidType.registration_id:
            push.audience = jpush.audience({'registration_id': [target]})
        elif cid_type == CidType.alias:
            push.audience = jpush.audience({'alias': [target]})
        else:
            raise CidTypeError('`CidType` type value `{}` unsupport.'
                               .format(cid_type.value))

        if self.client_system == ClientSystem.iOS:
            # 通知类型的使用 notification 而自定义消息使用 message
            if msg.push_type == PushType.notification:
                push.notification = jpush.notification(ios=msg.to_msg_object())
            elif msg.push_type == PushType.custom_message:
                push.message = jpush.message(msg.content, msg.title,
                                             extras=msg.custom_msg.get('extras', ''))
            else:
                raise SenderError(
                    'Unsupport push type: {}'.format(msg.push_type.name))
            push.platform = ['ios']
            push.options = {
                "apns_production": True if msg.environment == Environment.production else False}
        elif self.client_system == ClientSystem.Android:
            if msg.push_type == PushType.notification:
                push.notification = jpush.notification(android=msg.to_msg_object())
            elif msg.push_type == PushType.custom_message:
                push.message = jpush.message(msg.content, msg.title,
                                             extras=msg.custom_msg.get('extras', ''))
            else:
                raise SenderError(
                    'Unsupport push type: {}'.format(msg.push_type.name))
            push.platform = ['android']
        else:
            raise SenderError(
                'Unsupport client system type: {}.'.format(self.client_system.name))
        try:
            response = push.send()
        except Exception, e:
            return PushResult(PushExcetion(e))
        if response.status_code != 200:
            return PushResult(UnknowPushState(response.payload))
        else:
            return PushResult(Success(response.payload))
