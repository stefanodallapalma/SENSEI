from utils.ServerUtils import stop_server, is_running

flask_name = "flask_app.py"
celery_name = "celery_app.py"

if __name__ == '__main__':
    if is_running(flask_name):
        stop_server(flask_name)

    if is_running(celery_name):
        stop_server(celery_name)