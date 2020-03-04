# Standard library imports
import psutil, sh, os, subprocess

# Local application imports
from utils.bean.GrepProcess import GrepProcess


def kill_process(pid):
    if type(pid) is str:
        pid = int(pid)

    process = psutil.Process(pid)
    process.terminate()


def grep_process_list(keyword, abs_path=False):
    proc_list = sh.grep(sh.ps('aux', _piped=True), keyword)

    grep_list = []
    for proc in proc_list:
        # Convert multiple spaces in single spacw
        proc = " ".join(proc.split())

        proc = proc.split(" ")
        grep = GrepProcess()
        commands = []

        for i in range(len(proc)):
            if i == 0:
                grep.user = proc[i]
            elif i == 1:
                grep.pid = proc[i]
            elif i == 2:
                grep.cpu = proc[i]
            elif i == 3:
                grep.mem = proc[i]
            elif i == 4:
                grep.vsz = proc[i]
            elif i == 5:
                grep.rss = proc[i]
            elif i == 6:
                grep.tty = proc[i]
            elif i == 7:
                grep.stat = proc[i]
            elif i == 8:
                grep.start = proc[i]
            elif i == 9:
                grep.time = proc[i]
            else:
                commands.append(proc[i])

        if commands:
            grep.commands = commands

        grep_list.append(grep)

    if not abs_path:
        for auxgrep in grep_list:
            commands = auxgrep.commands
            new_commands = []
            for command in commands:
                if os.path.sep in command:
                    split = command.split(os.path.sep)
                    new_commands.append(split[len(split) - 1])
                else:
                    new_commands.append(command)

            auxgrep.commands = new_commands

    return grep_list


def execute_python3_code(path, wait=False):
    commands = ["python3", path]
    process = subprocess.Popen(commands, shell=False)

    if wait:
        process.wait()

    return process