# *-* coding: utf-8 *-*

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import (
    Column,
    String,
)

from settings import MYSQL_DB_CONFIG


class BaseModelMixin(object):
    """为所有Model提供公用方法"""

    @declared_attr
    def id(self):
        return  Column(String(32), primary_key=True)

    def select(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

base_model_map = {}

for db in MYSQL_DB_CONFIG['master']:
    # 生成ORM基类
    base_model_map[db] = declarative_base(cls=BaseModelMixin)