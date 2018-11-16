# *-* coding: utf-8 *-*

from handler.test import (
    SynchronousRequestHandler,
    GenCoroutinesRequestHandler,
    NativeCoroutinesRequestHandler
)


map_list = [
    (r'/sync', SynchronousRequestHandler),
    (r'/gen-coroutines', GenCoroutinesRequestHandler),
    (r'/native-coroutines', NativeCoroutinesRequestHandler),
]