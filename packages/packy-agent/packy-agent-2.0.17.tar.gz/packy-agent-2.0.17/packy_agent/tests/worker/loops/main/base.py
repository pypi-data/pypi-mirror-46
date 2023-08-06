import gevent


from packy_agent.worker.loops.main import MainLoop


def start_main_loop(tasks):
    main_loop = MainLoop(tasks)
    gevent.spawn(main_loop.run)
    gevent.sleep(1)
    assert main_loop.is_running
    return main_loop


def stop_main_loop(main_loop, timeout=2):
    main_loop.stop()
    gevent.sleep(timeout)
    assert not main_loop.is_running


def run_main_loop(tasks, stop_tasks=True, duration_seconds=2, stop_timeout=2):
    main_loop = start_main_loop(tasks)
    gevent.sleep(duration_seconds)
    if stop_tasks:
        for task in main_loop.tasks:
            task.stop()

        gevent.sleep(stop_timeout)
        for task in main_loop.tasks:
            assert not task.is_running

    stop_main_loop(main_loop, stop_timeout)
