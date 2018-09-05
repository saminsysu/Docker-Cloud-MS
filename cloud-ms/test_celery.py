import docker_tools
import time
while True:
    # task3 to queue3
    docker_tools.task3.apply_async()
    # task2 to queue2
    docker_tools.task2.apply_async()
    # task3 to queue-default
    docker_tools.task1.apply_async()
    # topic task
    docker_tools.task4.apply_async()
    docker_tools.task5.apply_async() # 或 docker_tools.task5.apply_async(queue="queue_5") 可以达到同样的效果
    time.sleep(2)
