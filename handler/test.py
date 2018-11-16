# *-* coding: utf-8 *-*

from tornado.gen import coroutine

from base.handler import BaseHandle
from controller.user import UserCtrl


class SynchronousRequestHandler(BaseHandle):
    def get(self):
        count = UserCtrl.sync_request()

        self.write('{} users1 so far!'.format(count))


class GenCoroutinesRequestHandler(BaseHandle):
    @coroutine
    def get(self):
        count = yield UserCtrl.gen_request()

        self.write('{} users2 so far!'.format(count))


class NativeCoroutinesRequestHandler(BaseHandle):
    async def get(self):
        count = await UserCtrl.native_request()

        self.write('{} users3 so far!'.format(count))
