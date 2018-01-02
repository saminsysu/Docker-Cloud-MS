import docker_tools
import time
while True:
    # task3 to queue3
    docker_tools.task3.apply_async()
    # task2 to queue2
    docker_tools.task2.apply_async()
    # task3 to queue-default
    docker_tools.task1.apply_async()
    time.sleep(2)