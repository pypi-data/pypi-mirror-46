# -*- coding:utf-8 -*-

import json
import uuid
import base64
import calendar
from datetime import date, datetime

try:
    ObjectId = getattr(__import__('bson'), 'ObjectId')
except ImportError:
    ObjectId = None


def _check_obj(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        ret = obj
    elif isinstance(obj, bytes):
        try:
            ret = obj.decode('utf-8')
        except UnicodeDecodeError:
            ret = 'BASE64:{}'.format(base64.b64encode(obj).decode('utf-8'))
    elif isinstance(obj, tuple):
        ret = _check_obj(list(obj))
    elif isinstance(obj, list):
        ret = list()
        for i in range(len(obj)):
            ret.append(_check_obj(obj[i]))
    elif isinstance(obj, dict):
        ret = dict()
        for k, v in obj.items():
            ret[str(k)] = _check_obj(v)
    elif isinstance(obj, date):
        if isinstance(obj, datetime):
            ret = calendar.timegm(obj.timetuple())
        else:
            ret = '{0:04}-{1:02}-{2:02}'.format(obj.year, obj.month, obj.day)
    elif isinstance(obj, uuid.UUID):
        ret = str(obj)
    elif ObjectId is not None and isinstance(obj, ObjectId):
        ret = str(obj)
    else:
        ret = str(obj.__class__.__name__)

    return ret


load = json.load
dump = json.dump


def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
    return json.loads(s,
                      encoding=encoding,
                      cls=cls,
                      object_hook=object_hook,
                      parse_float=parse_float,
                      parse_int=parse_int,
                      parse_constant=parse_constant,
                      object_pairs_hook=object_pairs_hook,
                      **kw)


def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
    return json.dumps(_check_obj(obj),
                      skipkeys=skipkeys,
                      ensure_ascii=ensure_ascii,
                      check_circular=check_circular,
                      allow_nan=allow_nan,
                      cls=cls,
                      indent=indent,
                      separators=separators,
                      default=default,
                      sort_keys=sort_keys,
                      **kw)
