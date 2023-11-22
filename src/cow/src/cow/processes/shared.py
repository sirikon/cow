import multiprocessing

ctx = multiprocessing.get_context("fork")
project_refresh_queue = ctx.Queue()
