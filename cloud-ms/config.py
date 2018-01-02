#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from kombu import Queue, Exchange

basedir = os.path.dirname(os.path.abspath(__file__))

def get_env(key):
    return os.environ.get(key, None)

# class CeleryConfig:
    # celery
    # broker_url = get_env('BROKER_URL')
    # exchange1 = Exchange('exchange1', 'direct')
    # exchange2 = Exchange('exchange2', 'direct')
    # task_queues = (
    #     Queue('queue_1', exchange1, routing_key='key1'),
    #     Queue('queue_2', exchange2, routing_key='key2'),
    #     Queue('queue_3', exchange2, routing_key='key3'),
    #     Queue('default', exchange=Exchange('default', 'direct'), routing_key='default'),
    # )
    # task_routes = {
    #     'docker_tools.operate_container': {
    #         'queue': 'queue_1',
    #         # 'exchange': 'exchange1',
    #         'routing_key': 'key1'
    #     },
    #     'docker_tools.task2': {
    #         'queue': 'queue_2',
    #         # 'exchange': 'exchange2',
    #         'routing_key': 'key2'
    #     },
    #     'docker_tools.task3': {
    #         'queue': 'queue_3',
    #         # 'exchange': 'exchange2',
    #         'routing_key': 'key3'
    #     }
    # }
    # task_default_exchange = 'default'
    # task_default_routing_key = 'default'
    # task_default_exchange_type = 'direct'
    # task_default_queue = 'default'

class Config:
    SECRET_KEY = get_env('SECRET_KEY')

    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_env('SQLALCHEMY_DATABASE_URI')


    # logging config
    LOG_CONFIG = os.path.join(basedir, 'etc', 'logging.ini')

    @classmethod
    def init_app(cls, app):
        pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    pass

config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}