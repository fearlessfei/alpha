# *-* coding: utf-8 *-*

import abc
import six
import importlib
import logging

from base.model import base_model_map
from core.db_manager import dbm
from settings import MYSQL_DB_CONFIG

logger = logging.getLogger()

ROUTE_LIST = []


@six.add_metaclass(abc.ABCMeta)
class LoaderBase:
    """加载者基类"""

    @abc.abstractmethod
    def load(self):
        raise NotImplementedError(
            "load method not implemented in {}.".format(self.__class__)
        )


class ModelLoader(LoaderBase):
    def __init__(self):
        self.engine = dbm.get_engine('master', 'sqlam')
        self.model_dir = 'models'

    def load(self):
        """
        把所有model都初始化一遍，为创建表做准备
        :return:
        """
        mod_list = load_path_mod(self.model_dir)
        logger.info('model: {}'.format(mod_list))

        for mod in mod_list:
            importlib.import_module('{}.{}'.format(self.model_dir, mod))

        # 创建表结构
        for db in MYSQL_DB_CONFIG['master']:
            base_model = base_model_map[db]
            engine = dbm.get_engine('master', db)

            logger.info('{} {}'.format(base_model, engine))

            base_model.metadata.create_all(engine)


class RouteLoader(LoaderBase):
    def __init__(self):
        self.route_dir = 'route'

    def load(self):
        global ROUTE_LIST

        mod_list = load_path_mod(self.route_dir)
        logger.info('route: {}'.format(mod_list))

        for mod in mod_list:
            m = importlib.import_module('{}.{}'.format(self.route_dir, mod))
            if not getattr(m, 'map_list', None):
                logger.info('Warning: {} Not defined map_list'.format(m))
                continue

            logger.info('route list: {}'.format(m.map_list))
            ROUTE_LIST.extend(list(set(m.map_list)))


def load_path_mod(dir):
    """
    加载对应路径模块
    :param dir: 目录
    :return:
    """
    import os

    mod_list = []
    model_path = os.path.dirname(__file__)
    for filename in os.listdir(os.path.join(model_path, dir)):
        name, extension = os.path.splitext(filename)
        if extension in ('.pyc', '.pyo') or name.startswith('__'):
            continue

        mod_list.append(name)

    return mod_list


def load():
    _globals = globals()
    for loader in _globals.values():
        if type(loader) is abc.ABCMeta and loader is not LoaderBase:
            logger.info('------------ load: {} -------------'.format(loader))

            loader().load()
