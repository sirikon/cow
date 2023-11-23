import multiprocessing
from os import getpid, makedirs
from os.path import join
from contextlib import redirect_stdout, redirect_stderr

from cow.processes.shared import ctx, project_refresh_queue
from cow.di import docker_project_manager, paths_provider


def worker(q: multiprocessing.Queue):
    pid = str(getpid())
    makedirs(paths_provider.logs, exist_ok=True)
    log_path = join(paths_provider.logs, f"worker.out")
    with open(log_path, "w", buffering=1) as output:
        with redirect_stdout(output):
            with redirect_stderr(output):
                print(f"================== Started worker. PID: {pid}")
                try:
                    while True:
                        print(f"================== Waiting for projects to refresh")
                        project_name = q.get()
                        print(f"================== Refreshing: {project_name}")
                        for text in docker_project_manager.refresh(project_name):
                            print(text, end="")
                        print("")
                        print("================== Refresh done")
                except KeyboardInterrupt:
                    pass


def spawn_worker():
    p = ctx.Process(target=worker, args=(project_refresh_queue,), daemon=True)
    p.start()
