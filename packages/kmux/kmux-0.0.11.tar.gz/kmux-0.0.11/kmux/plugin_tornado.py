# -*- coding:utf-8 -*-

import tornado
import tornado.web
import tornado.ioloop
from kmux.rest import Kmux, KmuxHTTPRequest, KmuxHTTPResponse, KmuxHandler


class KmuxTornadoHandler(tornado.web.RequestHandler):
    def get(self, *a, **kw):
        self.handle(*a, **kw)

    def put(self, *a, **kw):
        self.handle(*a, **kw)

    def post(self, *a, **kw):
        self.handle(*a, **kw)

    def head(self, *a, **kw):
        self.handle(*a, **kw)

    def patch(self, *a, **kw):
        self.handle(*a, **kw)

    def delete(self, *a, **kw):
        self.handle(*a, **kw)

    def options(self, *a, **kw):
        self.handle(*a, **kw)

    def handle(self, *a, **kw):
        request = KmuxHTTPRequest(
            method=self.request.method,
            url=self.request.full_url(),
            headers=dict(self.request.headers),
            body=self.request.body,
            request_uuid=None,
            request_time=None,
        )
        handler = KmuxHandler.create_handler(request)
        assert isinstance(handler, KmuxHandler)
        handler.handle()
        response = handler.get_response()
        assert isinstance(response, KmuxHTTPResponse)
        self.set_status(status_code=response.get_status())
        for (name, value) in response.get_headers().items():
            self.set_header(name, value)
        self.write(response.get_chunk())


class KmuxTornadoApplication(tornado.web.Application):
    def __init__(self, default_host=None, **settings):
        super(KmuxTornadoApplication, self).__init__([('.*', KmuxTornadoHandler)], default_host, None, **settings)

    def start(self, port=8080, host=None):
        Kmux().init()
        port = int(port)
        host = '0.0.0.0' if host is None else host
        self.listen(port=port, address=host)
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    from kmux.example import *
    app = KmuxTornadoApplication()
    app.start()
