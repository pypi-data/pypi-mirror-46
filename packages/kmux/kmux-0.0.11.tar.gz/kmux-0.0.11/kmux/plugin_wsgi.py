# -*- coding:utf-8 -*-

from kmux.rest import Kmux, KmuxHTTPRequest, KmuxHTTPResponse, KmuxHandler


def kmux_wsgi_application(environ, start_response):
    Kmux().init()

    request_headers = dict()
    header_prefix = 'HTTP_'
    for k, v in environ.items():
        if k.startswith(header_prefix):
            request_headers[k[len(header_prefix):]] = v

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    request_url = '{}://{}{}'.format(
        environ['wsgi.url_scheme'],
        environ['SERVER_NAME'],
        environ['PATH_INFO'],
    )
    if 'QUERY_STRING' in environ:
        request_url = '{}?{}'.format(request_url, environ['QUERY_STRING'])

    request = KmuxHTTPRequest(
        method=environ['REQUEST_METHOD'],
        url=request_url,
        headers=request_headers,
        body=request_body,
        request_uuid=None,
        request_time=None,
    )
    handler = KmuxHandler.create_handler(request)
    assert isinstance(handler, KmuxHandler)
    handler.handle()
    response = handler.get_response()
    assert isinstance(response, KmuxHTTPResponse)
    start_response(str(response.get_status()), response.get_headers().items())
    return [response.get_chunk()]


def __kmux_wsgi_application_example__(environ, start_response):
    __import__('example')
    return kmux_wsgi_application(environ, start_response)
