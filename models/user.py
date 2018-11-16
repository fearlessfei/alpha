# -*- coding:utf-8 -*-

from sqlalchemy import (
    Column,
    String,
)

from base.model import base_model_map
from settings import MYSQL_TEST1_DB

class User(base_model_map[MYSQL_TEST1_DB]):
    __tablename__ = 'user'

    name = Column(String(32))
    password = Column(String(64))

