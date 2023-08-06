# coding=utf-8

import config
import importlib
import logging
import pkgutil

import tornado.web
from .base_handler import BaseHandler
from tornado.web import StaticFileHandler


class Application(tornado.web.Application):
    def __init__(self):

        base_handlers = [
            (r'.*', BaseHandler),
            (r"/static/(.*)", StaticFileHandler, {"path": '/static'})
        ]

        settings = config.TornadoSettings

        tornado.web.Application.__init__(self, base_handlers, **settings)

    def load_routes(self, routes):
        """
        加载路由模块
        :param routes:
        """
        if routes is None:
            logging.info('invalid routes module')
            return

        for route in pkgutil.iter_modules(routes.__path__, routes.__name__ + "."):
            module_name = route[1]
            route_module = importlib.import_module(module_name)
            rs = route_module.routes
            if rs is None:
                continue

            logging.info('routes:[%s/*] added' % route_module.base)
            self.add_handlers(r'.*', rs)

        return self
