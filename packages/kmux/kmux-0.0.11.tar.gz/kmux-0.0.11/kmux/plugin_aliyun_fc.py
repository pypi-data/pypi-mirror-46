# -*- coding:utf-8 -*-

import kmux.jsonutils as json
from kmux.plugin_wsgi import kmux_wsgi_application
from kmux.rest import Kmux, KmuxHTTPRequest, KmuxHTTPResponse, KmuxHandler


def mux_aliyun_fc_handler(environ, start_response):
    return kmux_wsgi_application(environ, start_response)


def __mux_aliyun_fc_handler_example__(environ, start_response):
    __import__('example')
    return mux_aliyun_fc_handler(environ, start_response)


def mux_aliyun_fc_apigate_handler(event, context):
    Kmux().init()

    params = json.loads(event)
    headers = params['headers']
    assert isinstance(headers, dict)

    request_url = '{}://{}{}'.format(headers['X-Forwarded-Proto'], headers['CA-Host'], params['path'])
    query_params = params['queryParameters']
    if isinstance(query_params, dict) and len(query_params):
        request_url = '{}?{}'.format(request_url, '&'.join(['{}={}'.format(k, v) for (k, v) in query_params.items()]))

    request = KmuxHTTPRequest(
        method=params['httpMethod'],
        url=request_url,
        headers=headers,
        body=params['body'],
        request_uuid=None,
        request_time=None,
    )
    handler = KmuxHandler.create_handler(request)
    assert isinstance(handler, KmuxHandler)
    handler.handle()
    response = handler.get_response()
    assert isinstance(response, KmuxHTTPResponse)
    return json.dumps(dict(
        isBase64Encoded=False,
        statusCode=response.get_status(),
        headers=response.get_headers(),
        body=response.get_chunk(),
    ))


def __kmux_aliyun_fc_apigate_handler_example__(event, context):
    __import__('example')
    return mux_aliyun_fc_apigate_handler(event, context)
