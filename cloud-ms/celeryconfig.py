# -*- encoding: utf-8 -*-
import os
from kombu import Queue, Exchange

broker_url = os.environ.get('BROKER_URL', 'amqp://guest:guest@localhost:5672')
exchange1 = Exchange('exchange1', 'direct')
exchange2 = Exchange('exchange2', 'direct')
topic_exchange1 = Exchange('topic_exchange1', 'topic')
task_queues = (
    Queue('queue_1', exchange1, routing_key='key1'),
    Queue('queue_2', exchange2, routing_key='key2'),
    Queue('queue_3', exchange2, routing_key='key3'),
    Queue('queue_4', topic_exchange1, routing_key='topic1.#'),
    Queue('queue_5', topic_exchange1, routing_key='topic2.#'),
    Queue('default', exchange=Exchange('default', 'direct'), routing_key='default'),
)

# 这里没有指定exchange而是指定queue是因为celery会自动帮你根据task_queues中queue的定义查找对应的exchange，最终还是根据exchange和
# routing_key去路由task，再者，有些中间件没有定义exchange (比如redis)，所以这里定义queue会更通用
# 除了定义task_routes可以路由task，通过apply_async发送信息时指定queue也可以有效路由
task_routes = {
    'docker_tools.operate_container': {
        'queue': 'queue_1',
        # 'exchange': 'exchange1',
        # 'routing_key': 'key1'
    },
    'docker_tools.task2': {
        'queue': 'queue_2',
        # 'exchange': 'exchange2',
        # 'routing_key': 'key2'
    },
    'docker_tools.task3': {
        'queue': 'queue_3',
        # 'exchange': 'exchange2',
        # 'routing_key': 'key3'
    },
    'docker_tools.task4': {
        'queue': 'queue_4',
        # 'exchange': 'topic_exchange1',
        'routing_key': 'topic1.haha'
    },
    'docker_tools.task5': {
        'queue': 'queue_5',
        # 'exchange': 'topic_exchange1',
        'routing_key': 'topic2.haha'
    },
}

task_default_exchange = 'default'
task_default_routing_key = 'default'
task_default_exchange_type = 'direct'
task_default_queue = 'default'