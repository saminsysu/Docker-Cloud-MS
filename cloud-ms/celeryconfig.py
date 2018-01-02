# -*- encoding: utf-8 -*-
import os
from kombu import Queue, Exchange

broker_url = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672')
exchange1 = Exchange('exchange1', 'direct')
exchange2 = Exchange('exchange2', 'direct')
task_queues = (
    Queue('queue_1', exchange1, routing_key='key1'),
    Queue('queue_2', exchange2, routing_key='key2'),
    Queue('queue_3', exchange2, routing_key='key3'),
    Queue('default', exchange=Exchange('default', 'direct'), routing_key='default'),
)
task_routes = {
    'docker_tools.operate_container': {
        'queue': 'queue_1',
        # 'exchange': 'exchange1',
        'routing_key': 'key1'
    },
    'docker_tools.task2': {
        'queue': 'queue_2',
        # 'exchange': 'exchange2',
        'routing_key': 'key2'
    },
    'docker_tools.task3': {
        'queue': 'queue_3',
        # 'exchange': 'exchange2',
        'routing_key': 'key3'
    }
}
task_default_exchange = 'default'
task_default_routing_key = 'default'
task_default_exchange_type = 'direct'
task_default_queue = 'default'