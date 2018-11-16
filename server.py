# *-* coding: utf-8 *-*

from cgi import Server
from settings import (
    SETTINGS,
    LOG_CONFIG,
)


server = Server(**SETTINGS)

# 配置日志
server.set_logger(**LOG_CONFIG)

# 启动服务
server.start()
