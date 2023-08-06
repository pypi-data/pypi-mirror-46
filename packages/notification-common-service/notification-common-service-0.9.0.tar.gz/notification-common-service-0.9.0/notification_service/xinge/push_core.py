# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from xinge_push import (Message, Style, XingeApp, MessageIOS, TimeInterval,
                        ClickAction)

from notification_service.xinge import result_status
from notification_service.xinge.constant import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def _validate_push_params(accessId, secretKey, token, client_type, content,
                          title, msg_type, custom_info, environment):
    """
    对推送方法的参数进行校验
    :return: (error_code:int, error_msg:unicode)
        error_code 为 0，是成功
    """
    if accessId < 0 or not isinstance(accessId, int):
        return result_status.ACCESS_ID_ILLEGAL
    if not isinstance(secretKey, unicode):
        return result_status.SECRET_KEY_TYPE_ERROR
    if not isinstance(token, unicode):
        return result_status.TOKEN_TYPE_ERROR
    if client_type not in (
            CLIENT_TYPE_IOS,
            CLIENT_TYPE_ANDROID):
        return result_status.CLIENT_TYPE_ILLEGAL
    if not isinstance(content, unicode):
        return result_status.CONTENT_TYPE_ERROR
    if not isinstance(title, unicode):

        return result_status.TITLE_TYPE_ERROR
    if msg_type not in (
            MSG_TYPE_NOTIFICATION,
            MSG_TYPE_PENETRATE):
        return result_status.MSG_TYPE_ILLEGAL
    if not isinstance(custom_info, dict):
        return result_status.CUSTOM_INFO_TYPE_ERROR
    if environment not in (
            ENVIRONMENT_ANDROID,
            ENVIRONMENT_IOS_PRO,
            ENVIRONMENT_IOS_DEV):
        return result_status.ENVIRONMENT_ILLEGAL
    return result_status.SUCCESS


def _create_accept_time(time_plans):
    accept_time = []
    for plan in time_plans:
        if 'start' in plan and 'end' in plan:
            try:
                accept_time.append(TimeInterval(
                    int(plan['start']['hour']),
                    int(plan['start']['min']),
                    int(plan['end']['hour']),
                    int(plan['end']['min']),
                ))
            except:
                pass
    return accept_time


def _create_message_android(content, title, msg_type, custom_info):
    """
    生成需要发送的 Android 推送消息体
    :param content: 推送的主体内容
    :param title: 推送的标题
    :param custom_info: 推送定制信息
    :return: Message
    """
    msg = Message()
    msg.content = content
    msg.title = title
    msg.type = msg_type

    def _create_style(custom_info):
        """
        根据传入的字典创建 Style
        :param custom_info: 自定义信息
        :return: Style
        """
        style = Style()
        fields = {
            'title': 'title',
            'content': 'content',
            'builderId': 'builder_id',
            'ring': 'ring',
            'vibrate': 'vibrate',
            'clearable': 'clearable',
            'nId': 'n_id',
            'ringRaw': 'ring_raw',
            'lights': 'lights',
            'iconType': 'icon_type',
            'iconRes': 'icon_res',
            'styleId': 'style_id',
            'smallIcon': 'small_icon',
        }
        for key, value in fields.items():
            if value in custom_info:
                setattr(style, key, custom_info[value])
        return style

    msg.style = _create_style(custom_info)
    msg.acceptTime = _create_accept_time(custom_info.get('accept_time', ()))

    def _create_click_action(action):
        """
        根据传入的字典生成点击动作 action
        :param action: 动作的信息
        :return: ClickAction
        """
        if action == {} or 'action_type' not in action:
            return None
        click_action = ClickAction()
        click_action.actionType = action['action_type']
        if click_action.actionType == 1:
            click_action.activity = action.get('activity', '')
            click_action.intentFlag = action.get('aty_attr', {}).get('if', 0)
            click_action.pendingFlag = action.get('aty_attr', {}).get('pf', 0)
        elif click_action.actionType == 2:
            click_action.url = action.get('browser', {}).get('url', '')
            click_action.confirmOnUrl.get('browser', {}).get('confirm', 0)
        elif click_action.actionType == 3:
            click_action.intent = action.get('intent', '')
        else:
            raise ValueError('xinge push custom info action_type is illegal.')
        return click_action
    msg.action = _create_click_action(custom_info.get('action', {}))
    return msg


def _create_message_iOS(content, title, custom_info):
    """
    生成需要发送的 iOS 推送消息体

    信息体包含三种主要内容：
        1. APNs 相关的消息描述;
        2. 允许推送时间区间定制；
        3. 用户自定义键值对信息；
    :param content: 推送的主体内容
    :param title: 推送的标题
    :param custom_info: 推送定制信息
    :return: MessageIOS
    """
    msg = MessageIOS()
    aps = custom_info.pop('aps', {})
    alert = aps.get('alert', {})
    if 'title' not in alert:
        alert['title'] = title
    if 'body' not in alert:
        alert['body'] = content
    msg.alert = alert
    if 'badge' in aps:
        msg.badge = aps['badge']
    if 'category' in aps:
        msg.category = aps['category']
    msg.sound = aps.get('sound', 'default')

    msg.acceptTime = _create_accept_time(custom_info.pop('accept_time', ()))

    msg.custom = custom_info
    return msg


def push_single_device(accessId, secretKey, token, client_type, content,
                       title='通知', msg_type=MSG_TYPE_NOTIFICATION,
                       custom_info={}, environment=ENVIRONMENT_ANDROID):
    """
    对单一设备进行推送
    :param accessId: 等同于推送数据模型中 Server 的 app_id。
    :param secretKey: 等同于推送数据模型中 Server 的 app_secret
    :param token: 等同于推送数据模型中 Client 的 cid, 确定唯一设备
    :param client_type: 客户端类型，可选值为（xinge-ios, xinge-android）
    :param content: 推送的主体内容
    :param title: 推送标题
    :param msg_type: 推送类型,可选值（通知:1 ， 透传: 2）
    :param custom_info: 自定义通知参数
    :param environment: 向 iOS 设备推送时必填,1 表示推送生产环境;2 表示推送开发环境。
        推送 Android 平台不填或填 0。
    :return: (error_code:int, error_msg:unicode)
        error_code 为 0，是成功
    """
    # 校验数据
    try:
        accessId = int(accessId)
    except ValueError:
        return result_status.ACCESS_ID_NOT_NUMBER
    if client_type == CLIENT_TYPE_ANDROID:
        environment = ENVIRONMENT_ANDROID
    validate_result = _validate_push_params(accessId, secretKey, token,
                                            client_type, content, title,
                                            msg_type, custom_info, environment)
    if validate_result != result_status.SUCCESS:
        return validate_result

    # 构造推送信息体
    if client_type == CLIENT_TYPE_ANDROID:
        message = _create_message_android(
            content, title, msg_type, custom_info)
    elif client_type == CLIENT_TYPE_IOS:
        message = _create_message_iOS(content, title, custom_info)
    message.sendTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 推送
    app = XingeApp(accessId, secretKey)
    resp = app.CreateMultipush(message, environment=environment)
    if resp[0] == -1:
        return resp
    else:
        _, _, push_id = resp
        ret_code, error_msg = app.PushDeviceListMultiple(push_id, [token])
    return ret_code, error_msg, push_id


def check_authorization(accessId, secretKey):
    """
    检查 accessId 和 secretKey 是否能够通过验证
    :param accessId:
    :param secretKey:
    :return:
    """
    try:
        accessId = int(accessId)
    except ValueError:
        return False
    app = XingeApp(accessId, secretKey)
    try:
        (code, msg, _) = app.QueryDeviceCount()
    except ValueError:
        # 查询结果 SDK 无法加载为 JSON
        return True
    if code != 0:
        return False
    return True


__all__ = ['push_single_device', 'check_authorization']


if __name__ == '__main__':
    accessId = u'2100311092'
    secretKey = u'8d9bc98ffcdb833b369ae8ea72f8082c'
    token = u'4ebaca99000ec87349e64a5dbef6edbc19bb03a2'
    client_type = CLIENT_TYPE_ANDROID
    content = u'测试信鸽'
    title = u'通知标题'
    # result = push_single_device(accessId, secretKey, token, client_type, content, title)

    result = check_authorization(int(accessId), secretKey)
