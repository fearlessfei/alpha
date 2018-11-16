# *-* coding: utf-8 *-*

import logging
import tornado
import tornado.log
import tornado.ioloop
import tornado.web

import loader

logger = None


class Server:
    def __init__(self, *args, **kwargs):
        # 为启动服务做准备
        self.app = tornado.web.Application (loader.ROUTE_LIST, *args, **kwargs)

    def start(self, port=8888, *args, **kwargs):
        # 把所有需要初始化的先加载进来
        loader.load()

        self.app.listen(port, *args, **kwargs)

        logger.info('Server listen in {}'.format(port))

        tornado.ioloop.IOLoop.current().start()

    def set_logger(self, _logger='', level=logging.DEBUG, **format):
        global logger
        # 配置日志logger
        logger = logging.getLogger(_logger)
        tornado.log.enable_pretty_logging(logger=logger)

        # 设置日志输出格式
        if not format:
            format = dict(
                fmt='[%(asctime)s]%(color)s[%(levelname)s]%(end_color)s[%(module)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        fm = tornado.log.LogFormatter(**format)
        logger.handlers[0].setFormatter(fm)

        # 日志输入级别
        logger.setLevel(level)
