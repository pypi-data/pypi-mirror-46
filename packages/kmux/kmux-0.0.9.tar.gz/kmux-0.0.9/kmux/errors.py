# -*- coding:utf-8 -*-

import kmux.jsonutils as json


class KmuxError(Exception):
    def to_dict(self):
        raise NotImplementedError()

    def to_json(self):
        return json.dumps(self.to_dict())


class RestError(KmuxError):
    def __init__(self, code=500, reason='UNKNOWN', message='', data={}, debug=None):
        assert isinstance(code, int)
        assert isinstance(reason, str)
        assert isinstance(message, str)
        assert isinstance(data, (str, int, float, tuple, list, set, dict, bool)) or data is None
        assert isinstance(debug, (str, int, float, tuple, list, set, dict, bool)) or debug is None

        self.code = code
        self.reason = reason
        self.message = message
        self.data = data
        self.debug = debug
        self.request_uuid = None

    def to_dict(self):
        d = dict()
        d['code'] = self.code
        d['reason'] = self.reason
        d['message'] = self.message
        d['data'] = self.data
        d['request_uuid'] = self.request_uuid
        if self.debug is not None:
            d['debug'] = self.debug
        return d


class RestFinish(RestError):
    def __init__(self, data, code=0, reason='OK', message='OK', debug=None):
        super(RestFinish, self).__init__(
            code=code,
            reason=reason,
            message=message,
            data=data,
            debug=debug,
        )


class RestRawFinish(KmuxError):
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        d = dict()
        d['data'] = self.data
        return d
