import socket


def get_internal_ips():
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    return [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
