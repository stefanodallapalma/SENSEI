from socket import *


def scanner(host, port):
    if "https" in host:
        host = host.replace("https://", "")
    elif "http" in host:
        host = host.replace("http://", "")

    status = False

    s = socket(AF_INET, SOCK_STREAM)

    conn = s.connect_ex((host, int(port)))
    if conn == 0:
        status = True

    s.close()

    return status