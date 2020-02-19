from socket import *


def scanner(host, port):
    status = False

    s = socket(AF_INET, SOCK_STREAM)

    conn = s.connect_ex((host, port))
    print("Host: " + host)
    print("PORT: " + port)
    if (conn == 0):
        print("Port " + port + ": OPEN")
        status = True
    else:
        print("Port " + port + ": UNREACHABLE")

    s.close()

    return status