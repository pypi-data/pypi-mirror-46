#!/usr/bin/env python
from notification_service.jpush import common
import json

class Device(object):
    """Device info query/update..

    """
    def __init__(self, jpush):
        self._jpush = jpush
        self.entity = None

    def send(self, method, url, body, content_type=None, version=3):
        """Send the request

        """
        response = self._jpush._request(method, body,
            url, content_type, version=3)
        return DeviceResponse(response)

    def send2(self, method, url, body, content_type=None, version=3):
        response = self._jpush._request(method, body,
            url, content_type, version=3)
        return response.json()

    def get_taglist(self):
        """Get deviceinfo with registration id.
        """
        url = common.TAGLIST_URL
        body = None
        info = self.send2("GET", url, body)
        err  = info.get('error')
        if err:
            return {'errmsg': err.get('message')}
        return info

    def get_deviceinfo(self, registration_id):
        """Get deviceinfo with registration id.
        """
        url = common.DEVICE_URL + registration_id + "/"
        body = None
        info = self.send("GET", url, body)
        print (info)
        return info

    def set_deviceinfo(self, registration_id, entity):
        """Update deviceinfo with registration id.
        """
        url = common.DEVICE_URL + registration_id + "/"
        body = json.dumps(entity)
        info = self.send("POST", url, body)
        print (url), (body), (info)
        return info

    def delete_tag(self, tag, platform=None):
        """Delete registration id tag.
        """
        url = common.TAG_URL + tag + "/"
        body = None
        if platform:
            body = platform
        print (url), (body)
        info = self.send("DELETE", url, body)
        print (info)
        return info

    def update_tagusers(self, tag, entity):
        """Add/Remove specified tag users.
        """
        url = common.TAG_URL + tag + "/"
        body = json.dumps(entity)
        print (url), (body)
        info = self.send("POST", url, body)
        print (info)
        return info

    def check_taguserexist(self, tag, registration_id):
        """Check registration id whether in tag.
        """
        url = common.TAG_URL + tag + "/registration_ids/" + registration_id
        body = registration_id
        print (url), (registration_id)
        info = self.send("GET", url, body)
        print (info)
        return info

    def delete_alias(self, alias, platform=None):
        """Delete appkey alias.
        """
        url = common.ALIAS_URL + alias + "/"
        body = None
        if platform:
            body = platform
        print (url), (body)
        info = self.send("DELETE", url, body)
        print (info)
        return info

    def get_aliasuser(self, alias, platform=None):
        """Get appkey alias users.
        """
        url = common.ALIAS_URL + alias + "/"
        body = None
        if platform:
            body = platform
        print (url), (body)
        info = self.send("GET", url, body)
        print (info)
        return info

class DeviceResponse(object):
    """Response to a successful device request send.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    payload = None

    def __init__(self, response):
        if 0 != len(response.content):
            data = response.json()
            self.payload = data
        elif 200 == response.status_code:
            self.payload = "success"

    def __str__(self):
        return str(self.payload)
