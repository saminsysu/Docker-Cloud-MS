# -*- encoding: utf-8 -*-
import os
import sys
import re

//进入虚拟环境,相当于souce .venv/bin/active
activate_this = '/home/docker-server/Docker-Cloud-MS/.venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

//参照manage.py
//解决路径问题
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir)
sys.path.append(basedir)
sys.path.append(os.path.join(basedir, '..'))

//导入环境变量
env_file_path = os.path.join(basedir, '.env')
if os.path.exists(env_file_path):
    print('Importing environment from .env...')
    env = {}
    for line in open(env_file_path):
        line = line.strip()
        # Skip comments
        if re.match('^\s*#', line):
            continue
        try:
            idx = line.index('=')
        except:
            continue
        if idx+1 == len(line):
            continue
        env[line[:idx]] = line[idx+1:]
    os.environ.update(env)

from app import app as application