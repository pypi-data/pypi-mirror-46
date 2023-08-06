# coding=utf-8
from  notification_service import jpush

class Jiguang_Push(object):

    def __init__(self, app_key, master_secret):
        self.app_key = app_key
        self.master_secret = master_secret

    def set_alias(self, cid):
        # 设置jpush设备别名
        _jpush = jpush.JPush(self.app_key, self.master_secret)
        device = _jpush.create_device()
        alias = cid
        platform = "android,ios"
        device.get_aliasuser(alias, platform)

    def push_client_message(self, cid, content, title="通知"):
        _jpush = jpush.JPush(self.app_key, self.master_secret)
        push = _jpush.create_push()
        push.audience = jpush.audience(
            jpush.alias(cid)
        )
        push.message = jpush.message(content, title)
        push.platform = jpush.all_
        try:
            ret = push.send()
        except Exception, e:
            return {"error_msg": str(e)}
        return ret

    def push_single_device(self, cid, content, title="通知", type=1, client_type="jiguang-android", deploy_status=True, cid_type=1, extras_msg={}, jiguang_custom={}):
        _jpush = jpush.JPush(self.app_key, self.master_secret)
        push = _jpush.create_push()
        if cid_type == 1:
            push.audience = jpush.audience(
                jpush.alias(cid)
            )
        elif cid_type == 2:
            push.audience = jpush.audience(
                jpush.registration_id(cid)
            )
        android_msg = None
        ios_msg = None
        if client_type == "jiguang-ios":
            msg = {'title': title}
            if extras_msg:
                msg.update(extras_msg)
            ios_msg = jpush.ios(alert=content, badge="+1", sound="happy.caf", extras=msg)
            ios_custom = jiguang_custom.get('ios', {})
            if ios_custom:
                badge = ios_custom.get('badge')
                if badge is not None:
                    ios_msg['badge'] = badge
                sound = ios_custom.get('sound')
                if sound is not None:
                    ios_msg['sound'] = sound
                content_available = ios_custom.get('content-available')
                if content_available is not None:
                    ios_msg['content-available'] = content_available
                mutable_available = ios_custom.get('mutable-available')
                if mutable_available is not None:
                    ios_msg['mutable-available'] = mutable_available
                extras = ios_custom.get('extras', {})
                if extras:
                    ios_msg['extras'].update(extras)
                category = ios_custom.get('category')
                if category is not None:
                    ios_msg['category'] = category
        elif client_type == 'jiguang-android':
            msg = {'title': title}
            if extras_msg:
                msg.update(extras_msg)
            android_msg = jpush.android(alert=content, title=title, extras=msg)
            android_custom = jiguang_custom.get('android', {})
            if android_custom:
                builder_id = android_custom.get('builder_id')
                if builder_id is not None:
                    android_msg['builder_id'] = builder_id
                priority = android_custom.get('priority')
                if priority is not None:
                    android_msg['priority'] = priority
                category = android_custom.get('category')
                if category is not None:
                    android_msg['category'] = category
                alert_type = android_custom.get('alert_type')
                if alert_type is not None:
                    android_msg['alert_type'] = alert_type
                big_text = android_custom.get('big_text')
                if big_text is not None:
                    android_msg['big_text'] = big_text
                extras = android_custom.get('extras', {})
                if extras:
                    android_msg['extras'].update(extras)
                big_pic_path = android_custom.get('big_pic_path')
                if big_pic_path is not None:
                    android_msg['big_pic_path'] = big_pic_path
        if type == 1:
            push.notification = jpush.notification(alert=title, android=android_msg, ios=ios_msg)
        elif type == 2:
            custom_extras = {}
            if android_msg:
                android_extras = android_msg.get('extras')
                if android_extras:
                    custom_extras.update(android_extras)
            if ios_msg:
                ios_extras = ios_msg.get('extras')
                if ios_extras:
                    custom_extras.update(ios_extras)
            push.message = jpush.message(content, title, extras=custom_extras)
        push.platform = jpush.all_
        push.options = {"apns_production": deploy_status}
        try:
            ret = push.send()
        except Exception, e:
            return {"error_msg": str(e)}
        return ret
