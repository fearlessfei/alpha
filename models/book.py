# -*- coding:utf-8 -*-

from sqlalchemy import (
    Column,
    String,
)

from base.model import base_model_map
from settings import MYSQL_TEST2_DB


class Book(base_model_map[MYSQL_TEST2_DB]):
    __tablename__ = 'book'

    name = Column(String(32))

