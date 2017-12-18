from . import main
from flask import render_template, jsonify, request
from .forms import CreateContainerForm
import docker_tools
import logging
from .. import db
from ..models import Container

logger = logging.getLogger(__name__)

@main.route('/', methods=['GET'])
def index():
    containers = Container.query.all()
    return render_template('main/index.html', containers=containers)

@main.route('/create_container', methods=['POST'])
def create_container():
    response = {
        'status': 'fail',
        'data': {}
    }
    form = CreateContainerForm()
    if form.validate_on_submit():
        username = form.username.data
        container_name = form.containername.data
        container_id, ports = docker_tools.create_container(username, container_name, "ubuntu:16.04", "tail -f /dev/null", mounts=[])
        # save container metadata in mysql
        container = Container()
        container.container_name = container_name
        container.username = username
        container.container_id = container_id
        container.ports = ports
        db.session.add(container)

        logger.info("Create container %s", container_name)

        response['status'] = 'success'
        response['data'] = {
            'container_id': container_id,
            'container_name': container_name,
            'username': username
        }
    return jsonify(response)

@main.route('/operate_container', methods=['DELETE', 'POST'])
def operate_container():
    response = {
        'status': 'fail',
        'data': {}
    }
    id = request.json.get('container_id', None)
    operation_type = request.json.get('operation_type', None)
    container = Container.query.filter_by(id=id).first()
    if container:
        container_id = container.container_id
        if operation_type:
            status = docker_tools.operate_container(container_id, operation_type)
            if status == 'success':
                logger.info("Successful to %s container %s", operation_type, container.container_name)
                if operation_type == 'delete':
                    db.session.delete(container)
            else:
                logger.info("Fail to %s container %s", operation_type, container.container_name)
            response['status'] = status
            response['data'] = {
                'container_name': container.container_name
            }
        else:
            logger.error("There is something wrong with operation type!")
    else:
        logger.error("Container %d doesn't exist!", id)
    return jsonify(response)

