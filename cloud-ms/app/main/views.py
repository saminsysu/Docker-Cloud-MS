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

@main.route('/operate_container', methods=['DELETE', 'POST'])
def operate_container():
    response = {
        'status': 'fail',
        'data': {}
    }
    if request.json:
        id = request.json.get('container_mid', None)
        operation_type = request.json.get('operation_type', None)
    else:
        operation_type = 'create'

    if operation_type == 'create':
        form = CreateContainerForm()
        if form.validate_on_submit():

            username = form.username.data
            container_name = form.containername.data

            # save container metadata in mysql，after success in creating container, update the container info in database
            container = Container()
            container.container_name = container_name
            container.username = username
            container.status = 'under creating'
            db.session.add(container)
            db.session.commit()

            logger.info("Create container %s" % container_name)

            # celery task
            docker_tools.operate_container.delay(container_mid=container.id, operation_type='create',
                                                 username=username,
                                                 container_name=container_name, image="ubuntu:16.04",
                                                 command="tail -f /dev/null", mounts=[])

            response['status'] = 'success'
            response['data'] = {
                'container_name': container_name,
                'username': username
            }

    else:
        container = Container.query.filter_by(id=id).first()
        if container:
            container_id = container.container_id
            if operation_type:
                if operation_type == 'delete':
                    db.session.delete(container)
                    id=None
                elif operation_type == 'start':
                    container.status = 'under starting'
                    db.session.add(container)
                elif operation_type == 'stop':
                    container.status = 'under stopping'
                    db.session.add(container)
                docker_tools.operate_container.delay(container_mid=id, container_id=container_id, operation_type=operation_type)
            else:
                logger.error("You need to specify operation type!")

            response['data'] = {
                'container_name': container.container_name
            }
        else:
            logger.error("Container %d doesn't exist!" % id)
    return jsonify(response)

