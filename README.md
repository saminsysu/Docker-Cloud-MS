# Docker-Cloud-MS

Docker Cloud Management System. Through this system, we can manage (create, delete, start, stop, restart, etc) containers which we build through docker.

## 功能说明

1. 用户注册、登陆、注销功能；（暂不提供）
2. 用户可以管理容器（创建、删除、重启等）；（暂只考虑一个用户的情况）
3. 用户可以选择创建指定镜像（ubuntu, mysql等）的容器；（暂只支持添加ubuntu系统镜像的容器）
4. 待定…

## 部署过程

先安装rabbit-mq、docker、docker-compose和virtualenv，然后（当前目录为Docker-Cloud-MS）

1. 使用virtualenv创建虚拟环境

    '''
    virtualenv .venv -p python3
    '''

2. 安装所需函数库

    '''
    pip install -r requirements.txt
    '''

3. cd docker，然后运行以下命令

    '''
    # 构造ubuntu镜像
    $ docker build -t cloud-ms/ubuntu:16.04 -f ubuntu-dockerfile .
    # 启动mysql容器
    $ docker-compose -f docker-compose.yml -p cloud-ms-db up -d
    '''

4. cd ../cloud-ms，然后执行

    '''
    python manage.py db upgrade
    python manage.py deploy
    python manage.py runserver
    python manage.py worker
    '''

5. 访问localhost:5000即可进入系统主页！
