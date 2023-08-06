#!/usr/bin/env python
# encoding: utf-8
import socket


def is_port_open(port: int = None, host: str = '127.0.0.1'):
    """
    Check whether a port is open or not.

    :param int port: port number
    :param str host: host ip or name
    :return: bool
    """
    s = socket.socket()
    s.settimeout(0.5)
    try:
        # s.connect_ex return 0 means port is open
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()


def is_port_free(port: int = None, host: str = '127.0.0.1'):
    """
    Check whether a port is free or not.

    :param int port: port number
    :param str host: host ip or name
    :return: bool
    """
    return not is_port_open(port, host)


def get_free_port(port: int = 10001, host: str = '127.0.0.1'):
    """
    Get a free port of local host.

    :param int port: default value
    :param str host: host ip or name
    :return: int
    """
    while port < 65536:
        if is_port_open(port, host):
            port += 1
        else:
            return port

    return None
