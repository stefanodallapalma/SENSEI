# Standard library imports
import sys, subprocess, os, sh, psutil

# Third party imports
from builtins import print

from celery.bin import worker

# Local application imports
from utils.ShellUtils import kill_process, grep_process_list


celery_args = ["python3", "celery_app"]


def check_celery_worker(script_exec_name):
    celery_proc = grep_process_list(script_exec_name)
    for proc in celery_proc:
        args_set = set(proc.commands)
        celery_args_set = set(celery_args)

        if celery_args_set.issubset(args_set):
            return True

    return False


def run_worker(celery_app, logfile=None, pidfile=None):
    worker_var = worker.worker(app=celery_app)
    option = {
        'broker': celery_app.conf.broker_url,
        'loglevel': 'INFO',
        'logfile': logfile,
        'pidfile': pidfile,
        'traceback': True
    }

    worker_var.run(**option)


def stop_worker(script_exec_name):
    celery_proc = grep_process_list(script_exec_name)

    # Retrieve pids to kill
    pids = []
    for proc in celery_proc:
        args_set = set(proc.commands)
        celery_args_set = set(celery_args)

        if celery_args_set.issubset(args_set):
            print(str(proc))
            pids.append(proc.pid)

    for pid in pids:
        kill_process(pid)