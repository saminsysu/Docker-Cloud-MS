#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import docker
import logging
import socket
from celery import current_app as celery
from app import db
from app.models import Container

logger = logging.getLogger(__name__)

def get_client():
    try:
        docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='1.32')
        return docker_client
    except:
        logger.error("Can not get a docker client!")
        return None

def get_all_containers():
    docker_client = get_client()
    try:
        containers = docker_client.containers.get_all_containers()
        logger.info("Successful to get all containers!")
        return containers
    except:
        logger.info("Fail to get all containers!")

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    _, port = s.getsockname()
    s.close()
    return port

def get_free_ports():
    ports = {}
    is_ssh_port = True
    for i in range(0, 5):
        port = get_free_port()
        if is_ssh_port:
            ports[port] = 22
        else:
            ports[port] = port
    return ports

def ports_to_str(ports):
    ports_str = ''
    first = True
    for c_p, h_p in ports.items():
        if not first:
            ports_str += ', '
        else:
            first = False
        ports_str += str(h_p) + '->' + str(c_p)
        if h_p == 22:
            ports_str += '(used for ssh)'
    return ports_str

# 当bind=True时，task对象会作为第一个参数自动传入
@celery.task(bind=True, name='operate_container', max_retries=3, default_retry_delay=2)
def operate_container(self, container_mid=None, container_id=None, operation_type=None, \
                      username=None, container_name=None, image=None, command=None, mounts=[]):
    '''
    :param container_mid: container id in mysql
    :param container_id: container id in docker
    :param operation_type:
    :param username:
    :param container_name:
    :param image:
    :param command:
    :param mounts:
    :return:
    '''
    status = 'fail'
    docker_client = get_client()

    if container_id:
        try:
            container = docker_client.containers.get(container_id)
            container_name = container.name
        except:
            logger.info("No such container %d" % container_id)
    if container_mid:
        try:
            c = Container.query.filter_by(id=container_mid).first()
        except:
            logger.info("No such container %d" % container_mid)
    if operation_type == 'create':
        ports = get_free_ports()
        try:
            container = docker_client.containers.run(image=image, hostname=username, name=container_name,
                                                     command=command, \
                                                     ports=ports, mounts=mounts, detach=True)
            logger.info("Successful to create container %s in docker" % container.name)

            # update container info

            if c:
                c.container_id = container.id
                c.ports = ports_to_str(ports)
                c.status = 'running'
                status = 'success'
                db.session.add(c)
            else:
                logger.error("Container %s doesn't exist" % container_name)
        except docker.errors.APIError as e:
            print(e)
            logger.error("Fail to create container %s" % container_name)
    elif operation_type == 'delete':
        try:
            # Remove the volumes associated with the container, and force the removal of a running container
            container.remove(v=True, force=True)
            logger.info("Successful to delete container %s" % container_name)
            status = 'success'
        except:
            logger.error("Fail to delete container %s" % container_name)
    elif operation_type == 'start':
        try:
            container.start()
            logger.info("Successful to start container %s" % container_name)
            status = 'success'
            if c:
                c.status = 'running'
                db.session.add(c)
            else:
                logger.error("Container %s doesn't exist" % container_name)
        except:
            logger.error("Fail to start container %s" % container_name)
    elif operation_type == 'stop':
        try:
            container.stop(timeout=5)
            logger.info("Successful to stop container %s" % container_name)
            status = 'success'
            if c:
                c.status = 'stopped'
                db.session.add(c)
        except:
            logger.error("Fail to stop %s" % container_name)
    else:
        logger.error("The operation type %s not known" % operation_type)
    if status == 'fail':
        self.retry()

