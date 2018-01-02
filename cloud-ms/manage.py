#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from flask_script import Manager
import os, sys, logging, re

logger = logging.getLogger(__name__)

basedir = os.path.dirname(os.path.abspath(__file__))
os.chdir(basedir)
sys.path.append(basedir)

env_file_path = os.path.join(basedir, '.env')
if os.path.exists(env_file_path):
    logger.info('Importing environment variables from .env')
    env = {}
    for line in open(env_file_path, encoding='utf-8'):
        # 去除头尾空白字符
        line = line.strip()
        # Skip comments
        if re.match('^\s*#', line):
            continue
        try:
            index = line.index('=')
        except:
            continue
        if index+1 == len(line):
            continue
        env[line[:index]] = line[index+1:]
    os.environ.update(env)

from app import app, db
from flask_migrate import Migrate, MigrateCommand
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from celery import Celery

# add support for Flask’s application contexts and hooking it (celery application) up with the Flask configuration
def make_celery(app):
    celery = Celery()
    # 两种配置方式都可以, 当使用current_app当当前没有app时，会使用
    # DEFAULT_CONFIG_MODULE = 'celeryconfig' os.environ.get('CELERY_CONFIG_MODULE', DEFAULT_CONFIG_MODULE)来获取
    # 配置模块，因而还是celery.config_from_object('celeryconfig')这种方式比较合理
    # celery.config_from_object('config:CeleryConfig')
    celery.config_from_object('celeryconfig')
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@manager.option('-l', '--loglevel', default='info', dest='loglevel', help='Log level')
@manager.option('-c', '--concurrency', default=8, dest='concurrency', help='Concurrency')
@manager.option('-Q', '--queues', default='celery', dest='queues', help='Queues')
@manager.option('-n', '--hostname', default='celery', dest='hostname', help='Hostname')
def worker(loglevel, concurrency, queues, hostname):
    argv = ['', '-l', loglevel, '-c', str(concurrency), '-Q', queues, '-n', hostname]
    # conf=celery.conf
    celery.worker_main(argv=argv)

@manager.command
def deploy():
    from app import models
    db.create_all()

@manager.command
def runserver():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    manager.run()