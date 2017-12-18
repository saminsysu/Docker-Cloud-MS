import docker
import logging
import socket

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
    for i in range(0, 5):
        port = get_free_port()
        ports[port] = port
    return ports

def ports_to_str(ports):
    ports_str = ''
    first = True
    print(ports)
    for c_p, h_p in ports.items():
        if not first:
            ports_str += ', '
        else:
            first = False
        ports_str += str(h_p) + '->' + str(c_p)
    return ports_str

def create_container(username, container_name, image, command, mounts=[]):
    docker_client = get_client()
    ports = get_free_ports()
    try:
        container = docker_client.containers.run(image=image, hostname=username, name=container_name, command=command, \
                                  ports=ports, mounts=mounts, detach=True)
        logger.info("Successful to create container %s", container.name)
        return container.id, ports_to_str(ports)
    except:
        logger.error("Fail to create container %s", container_name)

def operate_container(container_id, operation_type):
    status = 'fail'
    docker_client = get_client()
    container = docker_client.containers.get(container_id)
    container_name = container.name
    if operation_type == 'delete':
        try:
            # Remove the volumes associated with the container, and force the removal of a running container
            container.remove(v=True, force=True)
            logger.info("Successful to delete container %s", container_name)
            status = 'success'
        except:
            logger.error("Fail to delete container %s", container_name)
    elif operation_type == 'start':
        try:
            container.start()
            logger.info("Successful to start container %s", container_name)
            status = 'success'
        except:
            logger.error("Fail to start container %s", container_name)
    elif operation_type == 'stop':
        try:
            container.stop(timeout=5)
            logger.info("Successful to start container %s", container_name)
            status = 'success'
        except:
            logger.error("Fail to start container %s", container_name)
    else:
        pass
    return status

