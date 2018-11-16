# *-* coding: utf-8 *-*

import logging

# mysql配置，多主多从配置模式
MYSQL_TEST1_DB = 'sqlam'
MYSQL_TEST2_DB = 'sqlam2'

MYSQL_DB_CONFIG = {
    'master': {
        MYSQL_TEST1_DB : {
            'uri': [
                'mysql+pymysql://root:chinese@127.0.0.1:3306/{}'.format(MYSQL_TEST1_DB),
            ],
            'params': {
                'encoding': 'utf-8',
                'echo': False,
                'pool_size': 20,
                'pool_recycle': 3600,
            }
        },
        MYSQL_TEST2_DB: {
            'uri': [
                'mysql+pymysql://root:chinese@127.0.0.1:3306/{}'.format(MYSQL_TEST2_DB),
            ],
            'params': {
                'encoding': 'utf-8',
                'echo': False,
                'pool_size': 20,
                'pool_recycle': 3600,
            }
        },
    },
    'slave': {
        MYSQL_TEST1_DB : {
            'uri': [
                'mysql+pymysql://root:chinese@127.0.0.1:3306/{}'.format(MYSQL_TEST1_DB),
            ],
            'params': {
                'encoding': 'utf-8',
                'echo': True,
                'pool_size': 20,
                'pool_recycle': 3600,
            }
        },
        MYSQL_TEST2_DB: {
            'uri': [
                'mysql+pymysql://root:chinese@127.0.0.1:3306/{}'.format(MYSQL_TEST2_DB),
            ],
            'params': {
                'encoding': 'utf-8',
                'echo': True,
                'pool_size': 20,
                'pool_recycle': 3600,
            }
        },
    },
}

# app配置
SETTINGS = {
    'debug': True,
}

# 日志配置
LOG_CONFIG = {
    'level': logging.INFO
}