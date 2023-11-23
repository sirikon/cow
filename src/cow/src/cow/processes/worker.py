import multiprocessing

from cow.processes.shared import ctx, project_refresh_queue
from cow.di import docker_project_manager


def worker(q: multiprocessing.Queue):
    try:
        while True:
            print(f"================== Waiting for projects to refresh")
            project_name = q.get()
            print(f"================== Refreshing: {project_name}")
            for text in docker_project_manager.refresh(project_name):
                print(text, end="")
            print("")
    except KeyboardInterrupt:
        pass


def spawn_worker():
    p = ctx.Process(target=worker, args=(project_refresh_queue,), daemon=True)
    p.start()
