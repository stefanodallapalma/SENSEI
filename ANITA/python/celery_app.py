import os
from signal import *

# Local application imports
from taskqueue.celery.config import celery
from taskqueue.celery.utils import run_worker
from utils.ServerUtils import is_running, stop_server


if __name__ == '__main__':
    run_worker(celery, logfile="celery.log")