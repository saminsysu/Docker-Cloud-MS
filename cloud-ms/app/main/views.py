from . import main
from flask import render_template, jsonify
from .forms import CreateContainerForm
import docker_tools
import logging
from app import db

logger = logging.getLogger(__name__)

@main.route('/', methods=['GET'])
def index():
    containers = docker_tools.get_all_containers()
    return render_template('main/index.html', containers=containers)

@main.route('/container', methods=['POST'])
def create_container():
    response = {
        'status': 'fail',
        'data': {}
    }
    form = CreateContainerForm()
    dd = form.validate_on_submit()
    if form.validate_on_submit():
        username = form.username.data
        container_name = form.containername.data
        container_id = docker_tools.create_container(username, container_name, "ubuntu:16.04", \
                             "tail -f /dev/null", mounts=[])
        # create container
        response['status'] = 'success'
        response['data'] = {
            'container_id': container_id,
            'container_name': container_name,
            'username': username
        }
    return jsonify(response)
