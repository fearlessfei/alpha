# *-* coding: utf-8

import contextlib
import functools
import random
import traceback
import types

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from settings import MYSQL_DB_CONFIG


class BindNotExistsException(Exception):
    pass


class DatabaseNotExistsException(Exception):
    pass


class DatabaseConfigNoneException(Exception):
    pass


class EngineConfigNoneException(Exception):
    pass


class DBManager:
    def __init__(self):
        self.session_map = {}
        self.engine_map = {}
        self.create_session()

    def create_session(self):
        for kind in MYSQL_DB_CONFIG:
            dbs = MYSQL_DB_CONFIG[kind]

            self.session_map[kind] = {}
            self.engine_map[kind] = {}
            for db in dbs:
                uris = MYSQL_DB_CONFIG[kind][db]['uri']
                params = MYSQL_DB_CONFIG[kind][db]['params']

                self.session_map[kind][db] = []
                self.engine_map[kind][db] = []
                for uri in uris:
                    engine = self.create_engine(uri, params)
                    session = self.create_single_session(engine)

                    self.engine_map[kind][db].append(engine)
                    self.session_map[kind][db].append(session)

    def create_single_session(self, engine):
        session_factory = sessionmaker(bind=engine)
        # 使用了scoped_session 默认情况下，创建的session都是Thread-Local Scope，
        # 创建的session对象具体有两点变化： 1. 使用Session()创建的session对象都是一样的，
        # 这可以保证代码在不同的多次调用session()依然获得到相同的session 对象
        # 2. 使用Session()创建的session对象 是 Thread-local,
        # session在线程与线程之间没有任何联系
        session = scoped_session(session_factory)

        return session

    def get_session(self, bind=None, db=None):
        """
        获取session对象

        :param bind: 绑定到哪里，master为主，slave为从，默认为从
        :param db: 绑定到哪个库
        :return:
        """
        if bind not in self.engine_map:
            raise DatabaseNotExistsException('Bind {} is not exists, check your DB_SETTINGS'.format(bind))

        if db not in self.engine_map[bind]:
            raise DatabaseNotExistsException('Database {} is not exists, check your DB_SETTINGS'.format(db))

        session_list = self.session_map[bind][db]
        if len(session_list) < 1:
            raise DatabaseConfigNoneException('Database config is None, check your DB_SETTINGS')

        session = random.choice(session_list)
        return session


    def create_engine(self, uri, params):
        engine = create_engine(uri, **params)
        return engine

    def get_engine(self, bind=None, db=None):
        """
        获取engine对象

        :param bind: 绑定到哪里，master为主，slave为从，默认为从
        :return:
        """
        if bind not in self.engine_map:
            raise DatabaseNotExistsException('Bind {} is not exists, check your DB_SETTINGS'.format(bind))

        if db not in self.engine_map[bind]:
            raise DatabaseNotExistsException('Database {} is not exists, check your DB_SETTINGS'.format(db))

        engine_list = self.engine_map[bind][db]
        if len(engine_list) < 1:
            raise EngineConfigNoneException('Engine config is None, check your DB_SETTINGS')


        engine_list = self.engine_map[bind][db]
        engine = random.choice(engine_list)

        return engine


    @contextlib.contextmanager
    def session_ctx(self, bind=None, db=None):
        """
        获取session上下文

        :param bind: 绑定到哪里，master为主，slave为从，默认为从
        :param db: 绑定到哪个库
        :return:
        """
        db_session = self.get_session(bind, db)
        session = db_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()

    def with_session(self, bind):
        def wrapper(obj):
            def _wrapper(*args, **kwargs):
                db_session = self.get_session(bind)
                session = db_session()

                try:
                    # 其他装饰对象待实现
                    if type(obj) is types.FunctionType:
                        return functools.partial(obj, session, *args, **kwargs)()
                    else:
                        raise TypeError('Undesired type {}'.format(type(obj)))
                except:
                    traceback.print_exc()
                    if session:
                        session.rollback()
                finally:
                    if session:
                        session.commit()
                        session.expunge_all()
                        session.close()
            return _wrapper
        return wrapper


dbm = DBManager()
