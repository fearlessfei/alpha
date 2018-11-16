# *-* coding: utf-8 *-*

from tornado.gen import coroutine

from base.ctrl import BaseCtrl
from core.async_exec import as_future
from core.db_manager import dbm
from models.user import User


class UserCtrl(BaseCtrl):
    @classmethod
    def sync_request(cls):
        with dbm.session_ctx('master', 'sqlam') as session:
            count = session.query(User).count()

        return count

    @classmethod
    @coroutine
    def gen_request(cls):
        with dbm.session_ctx('master', 'sqlam') as session:
            count = yield as_future(session.query(User).count)

        return count

    @classmethod
    async def native_request(cls):
        with dbm.session_ctx('master', 'sqlam') as session:
            count = await as_future(session.query(User).count)

        return count