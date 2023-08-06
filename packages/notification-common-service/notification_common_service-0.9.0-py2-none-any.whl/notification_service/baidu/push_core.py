# encoding: utf-8
from Channel import *


class Baidu_Push:

    def __init__(self, apiKey, secretKey):
        self.apiKey = apiKey
        self.secretKey = secretKey

    def push_single_device(self, channel_id, content, title="通知", type=1, client_type="baidu-android", deploy_status=2, baidu_obj={}):
        c = Channel(self.apiKey, self.secretKey)
        data = {}
        msg_type = 1 if type == 1 else 0
        data["msg_type"] = msg_type
        data["channel_id"] = int(channel_id)
        if client_type == 'baidu-android':
            message = {
                "title": title,
                "description": content
            }
            if baidu_obj:
                notification_builder_id = baidu_obj.get('notification_builder_id')
                if notification_builder_id is not None:
                    message['notification_builder_id'] = notification_builder_id
                notification_basic_style = baidu_obj.get('notification_basic_style')
                if notification_basic_style is not None:
                    message['notification_basic_style'] = notification_basic_style
                open_type = baidu_obj.get('open_type')
                if open_type is not None:
                    message['open_type'] = open_type
                url = baidu_obj.get('url')
                if url is not None:
                    message['url'] = url
                pkg_content = baidu_obj.get('pkg_content')
                if pkg_content is not None:
                    message['pkg_content'] = pkg_content
        elif client_type == 'baidu-ios':
            message = {
                "title": title,
                "description": content,
                "aps": {
                    "sound": "happy.caf",
                    "content-available": True
                }
            }
            aps = baidu_obj.get('aps')
            if aps:
                sound = aps.get('sound')
                badge = aps.get('badge')
                if badge is not None:
                    message['aps']['badge'] = badge
                if sound is not None:
                    message['aps']['sound'] = sound
            data['deploy_status'] = deploy_status
        data['msg'] = json.dumps(message)
        ret = c.pushSingle(data)
        if ret.get('error_code'):
            return {'error_msg': ret.get('error_msg')}
        return ret

    def fetchTag(self):
        '''
        获取百度推送标签，以验证app_secret是否正确
        '''
        c = Channel(self.apiKey, self.secretKey)
        tag = c.fetchTag()
        if tag.get('error_msg'):
            return {"errmsg": tag.get('error_msg'), "error_code": tag.get('error_code')}
        return {}
