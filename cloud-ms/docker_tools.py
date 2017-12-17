import docker
import logging

logger = logging.getLogger(__name__)

ALL_PORTS = [i for i in range(50000, 60001)]

USED_PORTS_SLICE = []

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

def get_free_ports():
    global USED_PORTS_SLICE
    for s in range(0, 2000):
        if s in USED_PORTS_SLICE:
            continue
        USED_PORTS_SLICE.append(s)
    ports = {}
    for p in range(s * 5, s * 5 + 5):
        ports[str(p)] = p
    return ports

def create_container(username, container_name, image, command, mounts=[]):
    docker_client = get_client()
    ports = get_free_ports()
    try:
        container = docker_client.containers.run(image=image, hostname=username, name=container_name, command=command, \
                                  ports=ports, mounts=mounts, detach=True)
        logger.info("Successful to create container %s", container.name)
        return container.id
    except:
        logger.error("Fail to create container %s", container_name)

def delete_container(container_id):
    docker_client = get_client()
    container = docker_client.get(container_id)
    # Remove the volumes associated with the container, and force the removal of a running container
    try:
        container_name = container.name
        container.remove(v=True, force=True)
        logger.info("Successful to delete container %s", container_name)
    except:
        logger.error("Fail to delete container %s", container_name)