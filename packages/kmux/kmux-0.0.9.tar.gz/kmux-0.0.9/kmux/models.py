# -*- coding:utf-8 -*-

import re
from kmux.limits import *
from kmux.errors import RestError
from datetime import date, datetime
try:
    ObjectId = getattr(__import__('bson'), 'ObjectId')
except ImportError:
    ObjectId = None


PATTERN_BASE64 = re.compile(r'^[a-zA-Z0-9+/]+=?$')
PATTERN_DATE = re.compile(r'^(\d{1,4})-(\d{1,2})-(\d{1,2})$')
PATTERN_DATETIME = re.compile(r'^(\d{1,4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2}):(\d{1,2})$')


class KmuxField(object):
    def __init__(self, required=False, default=None, desc=u''):
        assert isinstance(required, bool)
        assert isinstance(desc, str)

        self._is_required = required
        self._default_value = default
        self._desc = desc

        assert self.is_valid_default(default)

    @property
    def is_required(self):
        return self._is_required

    @property
    def default_value(self):
        v = self._default_value
        if isinstance(v, dict):
            v = dict(v.items())
        elif isinstance(v, (list, set, tuple)):
            v = list(v)
        return v

    @property
    def desc(self):
        return self._desc

    @property
    def type_name(self):
        return self.__class__.__name__

    def is_valid_value(self, v):
        raise NotImplementedError()

    def is_valid_param(self, v):
        if v is None:
            ret = not self.is_required
        else:
            ret = self.is_valid_value(v)
        return ret

    def is_valid_default(self, v):
        return v is None or self.is_valid_param(v)

    def process_value(self, v):
        raise NotImplementedError()

    def process_param(self, v):
        return self.process_value(v)


class AnyField(KmuxField):
    def is_valid_value(self, v):
        return True

    def process_value(self, v):
        return v


if ObjectId is not None:
    class ObjectIdField(KmuxField):
        def is_valid_value(self, v):
            return ObjectId.is_valid(v)

        def process_value(self, v):
            return ObjectId(v)
else:
    class ObjectIdField(KmuxField):
        def is_valid_value(self, v):
            return False

        def process_value(self, v):
            return None


class Int32Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        if isinstance(v, (int, float)):
            v = int(v)
        else:
            v = int(float(v))
        return v


class Int64Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        if isinstance(v, (int, float)):
            v = int(v)
        else:
            v = int(float(v))
        return v


class UInt32Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        if isinstance(v, (int, float)):
            v = int(v)
        else:
            v = int(float(v))
        return v


class UInt64Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        if isinstance(v, (int, float)):
            v = int(v)
        else:
            v = int(float(v))
        return v


class Float32Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        return float(v)


class Float64Field(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        return float(v)


class TextField(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (str, int, float)):
            is_valid = True
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        return str(v)


class BoolField(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (bool, int, float)):
            is_valid = True
        elif isinstance(v, str):
            try:
                float(v)
                is_valid = True
            except ValueError:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        ret = False
        if isinstance(v, (bool, int, float)):
            ret = bool(v)
        elif isinstance(v, str):
            ret = bool(float(v))
        return ret


class DateField(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (date, datetime)):
            is_valid = True
        elif isinstance(v, (int, float)):
            if v >= 0:
                is_valid = True
            else:
                is_valid = False
        elif isinstance(v, str):
            if re.match(PATTERN_DATE, v):
                is_valid = True
            elif re.match(PATTERN_DATETIME, v):
                is_valid = True
            else:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        ret = v
        if isinstance(v, (date, datetime)):
            ret = date(year=v.year, month=v.month, day=v.day)
        elif isinstance(v, (int, float)):
            ret = date.fromtimestamp(v)
        elif isinstance(v, str):
            if isinstance(v, PATTERN_DATE):
                args = re.findall(PATTERN_DATE, v)[0][:3]
                args = [int(x) for x in args]
                ret = date(*args)
            elif isinstance(v, PATTERN_DATETIME):
                args = re.findall(PATTERN_DATETIME, v)[0][:3]
                args = [int(x) for x in args]
                ret = date(*args)
        return ret


class DatetimeField(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, (date, datetime)):
            is_valid = True
        elif isinstance(v, (int, float)):
            if v >= 0:
                is_valid = True
            else:
                is_valid = False
        elif isinstance(v, str):
            if re.match(PATTERN_DATE, v):
                is_valid = True
            elif re.match(PATTERN_DATETIME, v):
                is_valid = True
            else:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        ret = v
        if isinstance(v, datetime):
            ret = datetime(year=v.year, month=v.month, day=v.day, hour=v.hour, minute=v.minute, second=v.second)
        if isinstance(v, date):
            ret = datetime(year=v.year, month=v.month, day=v.day)
        elif isinstance(v, (int, float)):
            ret = datetime.fromtimestamp(v)
        elif isinstance(v, str):
            if re.match(PATTERN_DATE, v):
                args = re.findall(PATTERN_DATE, v)[0][:6]
                args = [int(x) for x in args]
                ret = datetime(*args)
            elif re.match(PATTERN_DATETIME, v):
                args = re.findall(PATTERN_DATETIME, v)[0][:6]
                args = [int(x) for x in args]
                ret = datetime(*args)
        return ret


class ListField(KmuxField):
    def __init__(self, required=False, default=None, item=None, desc=u''):
        super(ListField, self).__init__(required, default, desc)
        assert isinstance(item, KmuxField) or item is None
        self._item = item if isinstance(item, KmuxField) else AnyField()

    @property
    def item(self):
        return self._item  # type: KmuxField

    def is_valid_value(self, v):
        if isinstance(v, (list, tuple, set)):
            is_valid = True
            for x in v:
                if not self._item.is_valid_value(x):
                    is_valid = False
                    break
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        ret = list()
        if isinstance(v, (list, tuple, set)):
            for x in v:
                ret.append(self.item.process_value(x))
        return ret


class DictField(KmuxField):
    def __init__(self, required=False, default=None, items=None, desc=u''):
        super(DictField, self).__init__(required, default, desc)
        assert isinstance(items, dict) or items is None
        self._items = dict()
        if isinstance(items, dict):
            for (k, v) in items.items():
                assert isinstance(v, KmuxField)
                self._items[k] = v

    @property
    def items(self):
        return self._items  # type: KmuxField

    def is_valid_value(self, v):
        if isinstance(v, dict):
            is_valid = True
            for (k, v) in v.items():
                if k in self._items:
                    if not self._items[k].is_valid_param(v):
                        is_valid = False
                        break
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        ret = dict()
        if isinstance(v, dict):
            for (k, v) in v.items():
                if k in self._items:
                    ret[k] = self._items[k].process_param(v)
        return ret


class KmuxFile(dict):
    def __init__(self, data=b'', filename=None, content_type='application/unknown'):
        self.data = data
        self.filename = filename
        self.content_type = content_type

    @property
    def data(self):
        return self.get('data')

    @data.setter
    def data(self, v):
        self['data'] = v

    @property
    def filename(self):
        return self.get('filename')

    @filename.setter
    def filename(self, v):
        self['filename'] = v

    @property
    def content_type(self):
        return self.get('content_type')

    @content_type.setter
    def content_type(self, v):
        self['content_type'] = v


class FileField(KmuxField):
    def is_valid_value(self, v):
        if isinstance(v, KmuxFile):
            is_valid = True
        elif isinstance(v, dict):
            if isinstance(v.get('data'), str):
                is_valid = True
            else:
                is_valid = False
        else:
            is_valid = False
        return is_valid

    def process_value(self, v):
        if isinstance(v, KmuxFile):
            ret = v
        elif isinstance(v, dict):
            ret = KmuxFile(
                data=v.get('data', b''),
                filename=v.get('filename'),
                content_type=v.get('content_type', 'application/unknown')
            )
        else:
            ret = None
        return ret
