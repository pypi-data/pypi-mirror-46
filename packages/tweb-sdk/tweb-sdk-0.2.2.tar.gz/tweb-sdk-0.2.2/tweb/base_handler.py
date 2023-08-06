# coding=utf-8

from tornado.web import RequestHandler
from .error_exception import ErrException, ERROR


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write_error(404, 'Not found or not implement')

    def send_error(self, status_code=500, **kwargs):
        if self.is_api_mode():
            if 'exc_info' in kwargs:
                lang = self.request.headers.get("Accept-Language")
                if lang is not None:
                    lang = lang.split(',')[0][:2]
                else:
                    lang = 'en'

                exception = kwargs['exc_info'][1]
                if isinstance(exception, ErrException):
                    return self.write_error(exception.err.code(), exception.err.message(lang), exception.extra)
                else:
                    err = ERROR.E50000
                    return self.write_error(err.code(), err.message(lang), kwargs['exc_info'].__str__())
        RequestHandler.send_error(self, status_code, **kwargs)

    def write_error(self, code, msg=None, extra=None):
        if msg is None:
            msg = 'Unknown error'

        b = len(str(code)) - 3
        if b < 0:
            st_code = 500
        else:
            d = 1
            for i in range(b):
                d *= 10
            st_code = int(code / d)

        self.set_status(st_code)
        err_obj = {'code': code, 'message': msg}
        if extra is not None:
            err_obj['extra'] = extra

        self.finish({'error': err_obj})

    def is_api_mode(self):
        content_type = self.request.headers.get("content-type")
        return content_type is not None and content_type.find('application/json') >= 0
