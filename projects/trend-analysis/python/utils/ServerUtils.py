# Local application imports
from utils.ShellUtils import kill_process, grep_process_list

basic_args = ["python3"]


def is_running(name):
    args = list(basic_args)
    args.append(name)

    processes = grep_process_list(name)

    for proc in processes:
        print(str(proc))
        args_set = set(proc.commands)
        server_args_set = set(args)

        if server_args_set.issubset(args_set):
            return True

    return False


def stop_server(name, whitelist_pid=None):
    args = list(basic_args)
    args.append(name)

    processes = grep_process_list(name)

    # Retrieve pids to kill
    pids = []
    for proc in processes:
        args_set = set(proc.commands)
        server_args_set = set(args)

        if server_args_set.issubset(args_set):
            print(str(proc))
            pids.append(proc.pid)

    if whitelist_pid is not None:
        if type(whitelist_pid) is not list:
            pids.remove(str(whitelist_pid))
        else:
            pids = [pid for pid in pids if pid not in whitelist_pid]

    for pid in pids:
        kill_process(pid)