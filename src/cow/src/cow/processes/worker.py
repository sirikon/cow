import multiprocessing
from os import getpid, makedirs
from os.path import join
from contextlib import redirect_stdout, redirect_stderr

from cow.processes.shared import ctx, project_refresh_queue
from cow.di import docker_project_manager, paths_provider


def worker(q: multiprocessing.Queue):
    pid = str(getpid())
    makedirs(paths_provider.logs, exist_ok=True)
    with open(paths_provider.worker_logs, "a", buffering=1) as output:
        with redirect_stdout(output):
            with redirect_stderr(output):
                print(f"================== Started worker. PID: {pid}")
                try:
                    while True:
                        print(f"================== Waiting for projects to refresh")
                        project_name = q.get()
                        print(f"================== Refreshing: {project_name}")
                        try:
                            docker_project_manager.refresh(project_name)
                        except Exception as ex:
                            print(ex)
                        print("================== Refresh done")
                except KeyboardInterrupt:
                    pass


def spawn_worker():
    p = ctx.Process(target=worker, args=(project_refresh_queue,), daemon=True)
    p.start()
