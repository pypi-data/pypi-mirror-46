# -*- coding:utf-8 -*-

import re
import os
import uuid
import inspect
import kmux.jsonutils as json
from datetime import datetime
from urllib.parse import urlparse, parse_qsl
from kmux.errors import *
from kmux.models import *


class KmuxHTTPRequest(object):
    def __init__(self, method, url, headers=None, body=None, request_uuid=None, request_time=None):
        assert isinstance(method, str)
        assert isinstance(url, str)
        assert isinstance(headers, dict) or headers is None
        assert isinstance(body, bytes) or body is None
        assert isinstance(request_uuid, (str, uuid.UUID)) or request_uuid is None
        assert isinstance(request_time, datetime) or request_time is None
        url_info = urlparse(url)

        self.method = str(method.upper())
        self.url = str(url)
        self.scheme = str(url_info.scheme)
        self.path = str(url_info.path)
        self.query = str(url_info.query)
        self.headers = dict()
        self._headers_lower_cache = dict()
        if isinstance(headers, dict):
            for k, v in headers.items():
                self.headers[k] = str(v)
                self._headers_lower_cache[k.lower()] = str(v)
        self.body = body if isinstance(body, bytes) else b''
        self.request_uuid = str(
            request_uuid if isinstance(request_uuid, (str, uuid.UUID)) else uuid.uuid4()
        )
        self.request_time = request_time if isinstance(request_time, datetime) else datetime.utcnow()

    def get_header(self, name, default_value=None):
        return self._headers_lower_cache.get(name.lower(), default_value)

    def to_dict(self):
        d = dict()
        d['method'] = self.method
        d['url'] = self.url
        d['headers'] = self.headers
        d['body'] = self.body
        d['request_uuid'] = self.request_uuid
        d['request_time'] = self.request_time
        return d


class KmuxResponse(object):
    def __init__(self, data, code=0, reason='OK', message='OK', debug=None):
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

    def to_json(self):
        return str(json.dumps(self.to_dict()))  # type: str


class KmuxHTTPResponse(object):
    def __init__(self):
        self.status_code = 200
        self.headers = dict()
        self.chunk = ''

    def clear(self):
        self.status_code = 200
        self.headers = dict()
        self.chunk = ''

    def set_status(self, status_code):
        self.status_code = status_code

    def set_header(self, name, value):
        self.headers[name] = value

    def write(self, chunk):
        assert isinstance(chunk, (bytes, str))
        chunk_bin = chunk if isinstance(chunk, bytes) else chunk.encode('utf-8')
        assert isinstance(chunk_bin, bytes)
        self.chunk = chunk_bin

    def get_status(self):
        return self.status_code

    def get_headers(self):
        return self.headers

    def get_chunk(self):
        return self.chunk


def _register_auth(*a, **kw):
    def _func(fn, self, auth, *a0, **kw0):
        if hasattr(self, '__auth__') and callable(getattr(self, '__auth__')):
            self.__auth__(auth, *a0, **kw0)
        else:
            self.set_error(RestError(code=401, reason='UNAUTHORIZED'))
        return fn(self, *a0, **kw0)

    if len(a) == 1 and callable(a[0]):
        def _func1(self, *a1, **kw1):
            return _func(a[0], self, {}, *a1, **kw1)
        _func1.__name__ = a[0].__name__
        return _func1
    elif len(a) == 2 and callable(a[0]) and isinstance(a[1], dict):
        def _func2(self, *a2, **kw2):
            return _func(a[0], self, a[1], *a2, **kw2)
        _func2.__name__ = a[0].__name__
        return _func2


def _register_handler(func, schemes, methods, path, auth=False, params=None, **kw):
    assert callable(func)

    if isinstance(schemes, str):
        schemes = [schemes]
    assert isinstance(schemes, (list, tuple, set))
    schemes = list(set(schemes))
    for i in range(len(schemes)):
        assert isinstance(schemes[i], str)
        schemes[i] = schemes[i].upper()
        assert schemes[i] in ['HTTP', 'HTTPS']

    if isinstance(methods, str):
        methods = [methods]
    assert isinstance(methods, (list, tuple, set))
    methods = list(set(methods))
    for i in range(len(methods)):
        assert isinstance(methods[i], str)
        methods[i] = methods[i].upper()
        assert methods[i] in ['GET', 'PUT', 'POST', 'HEAD', 'PATCH', 'DELETE']

    assert isinstance(path, str) and re.match(r'/[^?#]*', path)

    assert isinstance(auth, (bool, dict))
    if isinstance(auth, dict):
        func_t = _register_auth(func, auth)
    elif auth:
        func_t = _register_auth(func)
    else:
        func_t = func

    def _func(*_a, **_kw):
        return func_t(*_a, **_kw)

    _func.func_name = func.__name__
    _func.__doc__ = func.__doc__

    func_params = inspect.getfullargspec(func).args
    if len(func_params) and func_params[0] == 'self':
        func_params = func_params[1:]

    path_params = re.findall(r'{([_a-zA-Z][_a-zA-Z0-9]*)}', path)
    assert len(path_params) == len(set(path_params))

    path_param_schemas = dict()
    params = dict() if params is None else params
    assert isinstance(params, dict)
    if 'params' not in func_params and len(params) > 0:
        raise Exception('ParamMissedInHandlerMethod: params, {} {}'.format(methods, params))

    url_pattern = path
    for path_param in path_params:
        try:
            assert (path_param in params)
        except AssertionError as e:
            raise Exception(
                "你必须在params中详细定义路径中出现的变量参数：{} @ {} {}".format(path_param, methods, path)
            )

        path_param_schema = params[path_param]
        assert (isinstance(path_param_schema, (KmuxField, tuple, list)))
        if isinstance(path_param_schema, KmuxField):
            if isinstance(path_param_schema, ObjectIdField):
                path_param_schema = (path_param_schema, r'[0-9a-z]{24}')
            elif isinstance(path_param_schema, (Int32Field, Int64Field)):
                path_param_schema = (path_param_schema, r'\-?\d+')
            elif isinstance(path_param_schema, (UInt32Field, UInt64Field)):
                path_param_schema = (path_param_schema, r'\d+')
            elif isinstance(path_param_schema, (Float32Field, Float64Field)):
                path_param_schema = (path_param_schema, r'\-?\d+\.\d+')
            elif isinstance(path_param_schema, TextField):
                path_param_schema = (path_param_schema, r'[^/?#]+')
            else:
                raise Exception('UnsupportedFieldInPathParam: {0}'.format(path_param_schema.__class__.__name__))

        assert (isinstance(path_param_schema, (tuple, list)))
        path_param_schema = list(path_param_schema)
        assert (len(path_param_schema) == 2)
        assert (isinstance(path_param_schema[0], KmuxField))
        assert (isinstance(path_param_schema[1], str))

        path_param_schemas[path_param] = path_param_schema

        url_pattern = url_pattern.replace('{%s}' % path_param, '(%s)' % path_param_schema[1])

        del params[path_param]

    _func.__origin_func__ = func
    _func.__func_params__ = func_params
    _func.__path_params__ = path_params
    _func.__request_params__ = params
    _func.__path_schemas__ = path_param_schemas
    _func.__request_path__ = path
    _func.__url_pattern__ = url_pattern
    _func.__http_schemes__ = schemes
    _func.__http_methods__ = methods
    _func.__auth__ = auth

    return _func


def GET(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'GET', path, auth, params, **kw)
    return wrapper


def PUT(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'PUT', path, auth, params, **kw)
    return wrapper


def POST(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'POST', path, auth, params, **kw)
    return wrapper


def HEAD(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'HEAD', path, auth, params, **kw)
    return wrapper


def PATCH(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'PATCH', path, auth, params, **kw)
    return wrapper


def DELETE(path, auth=False, params=None, **kw):
    def wrapper(func):
        return _register_handler(func, ['HTTP', 'HTTPS'], 'DELETE', path, auth, params, **kw)
    return wrapper


def REQUEST(path, auth=False, params=None, **kw):
    def wrapper(func):
        methods = kw.get('method', kw.get('methods', ['GET', 'PUT', 'POST', 'HEAD', 'PATCH', 'DELETE']))
        return _register_handler(func, ['HTTP', 'HTTPS'], methods, path, auth, params, **kw)
    return wrapper


class KmuxHandler(object):
    __handler_class__ = list()
    __handler_funcs__ = list()
    __handler_table__ = list()

    @classmethod
    def gen_func_url_patterns(cls):
        url_patterns = []
        for item in dir(cls):
            attr = getattr(cls, item)
            if callable(attr) and hasattr(attr, '__url_pattern__'):
                url_pattern = getattr(attr, '__url_pattern__')

                kmux_path_prefix = getattr(cls, '__KMUX_PATH_PREFIX__', None)
                if isinstance(kmux_path_prefix, str):
                    kmux_path_prefix = [kmux_path_prefix]
                elif isinstance(kmux_path_prefix, (tuple, set, list)):
                    kmux_path_prefix = list(set(kmux_path_prefix))
                else:
                    kmux_path_prefix = [None]

                assert isinstance(kmux_path_prefix, list)
                for path_prefix in kmux_path_prefix:
                    if isinstance(path_prefix, str):
                        full_url_pattern = '{}{}'.format(path_prefix, url_pattern)
                    else:
                        full_url_pattern = url_pattern

                    full_url_pattern_ex = re.compile('^{}$'.format(full_url_pattern))
                    cls.__handler_funcs__.append((full_url_pattern_ex, attr))
                    url_patterns.append(full_url_pattern_ex)
        url_patterns = list(set(url_patterns))
        return url_patterns

    @classmethod
    def gen_handler_url_patterns(cls):
        url_patterns = []

        for handler in cls.__handler_class__:
            assert (issubclass(handler, KmuxHandler))
            for url_pattern in handler.gen_func_url_patterns():
                url_patterns.append((url_pattern, handler))
        url_patterns.append((r'.*', HTTP404Handler))

        return url_patterns

    @classmethod
    def cls_init(cls):
        cls.__handler_table__ = cls.gen_handler_url_patterns()

    @classmethod
    def create_handler(cls, request):
        assert isinstance(request, KmuxHTTPRequest)
        handler = None
        for (url_pattern, handler_cls) in cls.__handler_table__:
            if re.match(url_pattern, request.path):
                handler = handler_cls(request)
                break
        if handler is None:
            handler = HTTP404Handler(request)
        return handler

    def __init__(self, request, *a, **kw):
        assert isinstance(request, KmuxHTTPRequest)
        self.request = request
        self.response = KmuxHTTPResponse()
        self.on_init(request)

    def on_init(self, request):
        pass

    def is_debug_mode(self):
        return False

    def get_response(self):
        return self.response

    def set_response(self, data=None):
        data = dict() if data is None else data
        raise RestFinish(data)

    def set_raw_response(self, data=None):
        data = '' if data is None else data
        raise RestRawFinish(data)

    def set_header(self, name, value):
        self.response.set_header(name, value)

    def set_status(self, status_code):
        self.response.set_status(status_code)

    def clear(self):
        self.response.clear()
        self.set_header('Content-Type', 'application/json;charset=UTF-8')
        self.set_header('Content-Language', 'zh-CN')
        self.set_header('Server', 'Kmux/1.0')

    def translate_reason(self, reason):
        return reason

    def process_debug_info(self, d):
        debug_info = None
        if self.is_debug_mode():
            debug_info = self.request.to_dict()
        setattr(d, 'debug', debug_info)

    def process_rest_response(self, d):
        assert isinstance(d, KmuxResponse)
        d.request_uuid = self.request.request_uuid
        self.process_debug_info(d)
        return d

    def process_rest_error(self, e):
        assert (isinstance(e, RestError))
        e.message = self.translate_reason(e.reason)
        e.request_uuid = self.request.request_uuid
        self.process_debug_info(e)
        return e

    def write_error(self, e):
        assert isinstance(e, RestError)
        self.write_dict(e.to_dict())

    def write_response(self, response):
        assert isinstance(response, KmuxResponse)
        self.write_dict(response.to_dict())

    def write_dict(self, d):
        assert isinstance(d, dict)
        self.response.write(json.dumps(d))

    def write_data(self, data):
        assert isinstance(data, (bytes, str))
        self.response.write(data)

    def set_error(self, e):
        assert isinstance(e, Exception)
        raise e

    def on_exception(self, e):
        import traceback

        self.clear()

        err = RestError(
            code=500,
            reason='SYS_{0}'.format(e.__class__.__name__),
            message=str(e),
            data={
                'type': str(type(e)),
                'args': e.args,
                'message': str(e),
                'traceback': traceback.format_exc().splitlines(),
            },
        )

        err = self.process_rest_error(err)

        self.write_error(err)

    def on_invalid_request_body(self):
        pass

    def on_invalid_param(self, name, field):
        raise RestError(
            code=400,
            reason='INVALID_PARAM',
            data={
                'param': {
                    'name': name,
                    'type': field.type_name,
                },
            }
        )

    def on_missing_required_param(self, name, field):
        raise RestError(
            code=400,
            reason='MISSING_REQUIRED_PARAM',
            data={
                'param': {
                    'name': name,
                    'type': field.type_name,
                },
            }
        )

    def get_current_user(self):
        return None

    def on_raw_response_data(self, data):
        if not isinstance(data, (bytes, str)):
            data = str(data)
        self.write_data(data)

    def on_response_data(self, data, message='OK'):
        self.clear()

        response = KmuxResponse(data, message=message if message else 'OK')
        response = self.process_rest_response(response)

        self.write_response(response)

    def on_rest_error(self, e):
        self.clear()

        err = self.process_rest_error(e)

        self.write_error(err)

    def on_not_handled(self):
        self.clear()

        err = RestError(
            code=404,
            reason='INVALID_REQUEST_URL',
        )
        err = self.process_rest_error(err)

        self.write_error(err)

    def on_options(self):
        self.clear()

    def handle(self, *a, **kw):
        try:
            self.__handle(*a, **kw)
        except Exception as e:
            self.on_exception(e)

    def __handle(self, *a, **kw):
        is_handled = False

        self.response.clear()

        request_method = self.request.method

        if request_method == 'OPTIONS':
            try:
                self.on_options()
            except RestRawFinish as e:
                self.on_raw_response_data(e.data)
            except RestFinish as e:
                self.on_response_data(e.data, e.message)
            except RestError as e:
                self.on_rest_error(e)
            except Exception as e:
                self.on_exception(e)
        else:
            for (pattern, func) in self.__handler_funcs__:
                if request_method in func.__http_methods__ and re.match(pattern, self.request.path):
                    is_handled = True
                    try:
                        _args = re.findall(pattern, self.request.path)
                        if len(_args) and isinstance(_args[0], (list, tuple, set)):
                            _args = _args[0]
                        _kwargs = dict(zip(func.__path_params__, _args))
                        for k in _kwargs.keys():
                            v = _kwargs[k]
                            (_field, _pattern) = func.__path_schemas__.get(k)
                            assert (isinstance(_field, KmuxField))
                            _kwargs[k] = _field.process_param(v)

                        content_type = self.request.headers.get('Content-Type', '')
                        assert isinstance(content_type, str)

                        d = dict()
                        if content_type.startswith('application/x-www-form-urlencoded'):
                            d = dict(parse_qsl(self.request.body.decode('utf-8')))
                        elif content_type.startswith('multipart/form-data'):
                            fields = content_type.split(';')

                            boundary = None
                            for field in fields:
                                k, sep, v = field.strip().partition('=')
                                if k == 'boundary' and v:
                                    boundary = v
                                    break

                            if not isinstance(boundary, str):
                                self.set_error(RestError(reason='INVALID_REQUEST'))

                            if boundary.startswith('"') and boundary.endswith('"'):
                                boundary = boundary[1:-1]
                            boundary = boundary.encode('utf-8')

                            boundary_t = b'--' + boundary + b'--'
                            final_boundary_index = self.request.body.rfind(boundary_t)
                            if final_boundary_index == -1:
                                self.set_error(RestError(reason='INVALID_REQUEST'))

                            boundary_t = b'--' + boundary + b'\r\n'
                            parts = self.request.body[:final_boundary_index].split(boundary_t)
                            for part in parts:
                                if not part:
                                    continue
                                eoh = part.find(b'\r\n\r\n')
                                if eoh == -1:
                                    self.set_error(RestError(reason='INVALID_REQUEST'))

                                part_headers = dict()
                                for header_line in part[:eoh].splitlines():
                                    header_kv = header_line.split(b':', 1)
                                    if len(header_kv) != 2:
                                        self.set_error(RestError(reason='INVALID_REQUEST'))
                                    header_k = header_kv[0].strip()
                                    header_v = header_kv[1].strip()
                                    if header_k == b'Content-Disposition':
                                        disp_items = header_v.split(b';')
                                        if len(disp_items) == 0:
                                            self.set_error(RestError(reason='INVALID_REQUEST'))
                                        elif disp_items[0].strip() != b'form-data':
                                            self.set_error(RestError(reason='INVALID_REQUEST'))
                                        disp_items = disp_items[1:]
                                        for disp_item in disp_items:
                                            disp_kv = disp_item.strip().split(b'=')
                                            if len(disp_kv) != 2:
                                                continue
                                            disp_k = disp_kv[0].strip()
                                            disp_v = disp_kv[1].strip()
                                            if disp_v.startswith(b'"') and disp_v.endswith(b'"'):
                                                disp_v = disp_v[1:-1]
                                            part_headers[disp_k.decode('utf-8')] = disp_v.decode('utf-8')
                                    else:
                                        part_headers[header_k.decode('utf-8')] = header_v.decode('utf-8')

                                if part_headers.get('name', None) is None:
                                    self.set_error(RestError(reason='INVALID_REQUEST'))

                                if part_headers.get('filename', None) is not None:
                                    d[part_headers['name']] = KmuxFile(
                                        data=part[eoh + 4:-2],
                                        filename=part_headers['filename'],
                                        content_type=part_headers.get('Content-Type', 'application/unknown')
                                    )
                                else:
                                    d[part_headers['name']] = part[eoh + 4:-2].decode('utf-8')
                        else:
                            try:
                                d = json.loads(self.request.body.strip())
                            except Exception:
                                d = dict(parse_qsl(self.request.body))

                        d_qs_t = dict(parse_qsl(self.request.query))
                        d_qs = dict()
                        for (k, v) in d_qs_t.items():
                            try:
                                vv = json.loads(v)
                            except ValueError:
                                vv = str(v)
                            d_qs[k] = vv

                        def process_d_qs(item):
                            assert isinstance(item, dict)
                            result_d = dict()

                            loop = True
                            while loop:
                                loop = False
                                remove_items = set()
                                item_keys = item.keys()
                                for kkk in item_keys:
                                    vvv = item[kkk]
                                    if len(kkk) and kkk[-1] == ']' and re.match(r'.+\[[^\[\]]+\]', kkk):
                                        remove_items.add(kkk)

                                        items = re.findall(r'(.+)\[(.+)\]', kkk)
                                        assert (len(items) == 1)
                                        items = items[0]
                                        assert (len(items) == 2)
                                        kkk = items[0]
                                        kkk2 = items[1]
                                        result_d.setdefault(kkk, {})
                                        result_d[kkk][kkk2] = vvv
                                        loop = True
                                    else:
                                        result_d[kkk] = vvv
                                for remove_item in remove_items:
                                    if remove_item in item:
                                        del item[remove_item]
                                item = result_d

                            return result_d

                        d_qs = process_d_qs(d_qs)
                        d = process_d_qs(d)

                        d.update(d_qs)

                        d, _d = {}, d
                        assert (isinstance(func.__request_params__, dict))
                        for (k, _field) in func.__request_params__.items():
                            assert (isinstance(k, str))
                            assert (isinstance(_field, KmuxField))
                            if k in _d:
                                try:
                                    d[k] = _field.process_param(_d[k])
                                except Exception:
                                    self.on_invalid_param(k, _field)
                            elif _field.is_required:
                                self.on_missing_required_param(k, _field)
                            else:
                                d[k] = _field.process_param(_field.default_value)

                        d.update(_kwargs)

                        _params = {
                            'me': self.get_current_user(),
                            'params': d,
                        }
                        for k in list(_params.keys()):
                            if k not in func.__func_params__:
                                del _params[k]

                        response_data = func(self, **_params)

                        self.on_response_data(response_data)
                    except RestRawFinish as e:
                        self.on_raw_response_data(e.data)
                    except RestFinish as e:
                        self.on_response_data(e.data, e.message)
                    except RestError as e:
                        self.on_rest_error(e)
                    except Exception as e:
                        self.on_exception(e)
                    break

            if not is_handled:
                self.on_not_handled()


class HTTP404Handler(KmuxHandler):
    def __handle(self, *a, **kw):
        self.on_not_handled()


class MockHandler(KmuxHandler):
    def mock(self, params, me):
        self.set_response({
            'message': 'just mock it'
        })


def REST(cls):
    assert(issubclass(cls, KmuxHandler))
    KmuxHandler.__handler_class__.append(cls)
    return cls


class Kmux(object):
    def __init__(self):
        pass

    @classmethod
    def load_apis(cls, filename):
        assert isinstance(filename, str)
        if filename.endswith('.json') and os.path.isfile(filename):
            with open(filename, 'r+') as fo:
                lines = fo.readlines()
                apis_doc = json.loads(''.join(lines))
            assert isinstance(apis_doc, dict)
            apis_env = apis_doc.get('env', {})
            apis_list = apis_doc.get('apis', [])
            assert isinstance(apis_env, dict)
            assert isinstance(apis_list, list)
            apis_env_KMUX_PATH_PREFIX = apis_env.get('KMUX_PATH_PREFIX', '')

            cls_table = dict()
            for i in [
                AnyField,
                ObjectIdField,
                Int32Field,
                Int64Field,
                Float32Field,
                Float64Field,
                DateField,
                DatetimeField,
                ListField,
                DictField,
                FileField,
            ]:
                cls_table[i.__name__[:-5]] = i

            for apis_item in apis_list:
                assert isinstance(apis_item, dict)
                api_schemes = ['HTTP', 'HTTPS']
                api_methods = [apis_item['method']]
                api_path = apis_env_KMUX_PATH_PREFIX + apis_item['path']
                api_auth = apis_item.get('auth', False)
                api_params_t = apis_item.get('params', {})
                api_params = dict()
                for k, v in api_params_t.items():
                    assert isinstance(k, str)
                    assert isinstance(v, dict)
                    api_param_field_cls = cls_table[v['type']]
                    api_param_field_kw = {
                        'required': v.get('required', False),
                        'default': v.get('default', None),
                        'desc': v.get('desc', ''),
                    }
                    api_params[k] = api_param_field_cls(**api_param_field_kw)
                func_mock = _register_handler(MockHandler.mock, api_schemes, api_methods, api_path, api_auth, api_params)
                setattr(MockHandler, 'mock-{}'.format(uuid.uuid4()), func_mock)

    def init(self):
        KmuxHandler.__handler_class__.append(MockHandler)
        KmuxHandler.cls_init()
