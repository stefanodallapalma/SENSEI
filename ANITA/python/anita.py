import sys
from signal import *
from utils.ShellUtils import execute_python3_code
from utils.ServerUtils import stop_server

flask_name = "flask_app.py"
celery_name = "celery_app.py"


def clean(*args):
    stop_server(celery_name)
    stop_server(flask_name)
    sys.exit(0)


if __name__ == "__main__":
    SIGNAL_LIST = [SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM]
    if sys.platform == "linux" or sys.platform == "darwin":
        try:
            SIGNAL_LIST.append(SIGBREAK)
        except NameError:
            pass

    for sig in SIGNAL_LIST:
        signal(sig, clean)

    execute_python3_code(celery_name)
    execute_python3_code(flask_name)