# -*- coding:utf-8 -*-

from kmux.rest import KmuxHandler, REST, GET, POST, REQUEST, Kmux
from kmux.rest import Int32Field


class ExampleHandler(KmuxHandler):
    def is_debug_mode(self):
        return True


@REST
class WelcomeHandler1(ExampleHandler):
    @GET('/')
    def hello(self):
        self.set_response({
            'message': 'hello world'
        })

    @GET('/test/bin')
    def test_bin(self):
        self.set_header('Content-Type', 'text/html')
        self.set_raw_response(b'hello world')

    @GET('/test/html')
    def test_html(self):
        self.set_header('Content-Type', 'text/html')
        self.set_raw_response('<p style="color:#F00;">hello html</p>')

    @REQUEST('/test/request')
    def test_request(self):
        self.set_response({
            'message': 'test request, {}'.format(self.request.method)
        })


@REST
class WelcomeHandler2(ExampleHandler):
    @POST('/add', params=dict(
        x=Int32Field(required=True),
        y=Int32Field(required=True),
    ))
    def add(self, params):
        x = params['x']
        y = params['y']
        z = x + y
        self.set_response({
            'result': z
        })
