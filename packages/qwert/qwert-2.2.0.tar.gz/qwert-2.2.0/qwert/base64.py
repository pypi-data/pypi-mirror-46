#!/usr/bin/env python
# encoding: utf-8
import base64


def encode(s, urlsafe: bool = False):
    """
    Base64 encode.

    :param s:
    :param urlsafe: Whether use URL Safe Mode
    :return: str
    """
    if isinstance(s, str):
        s = s.encode('utf-8')

    if urlsafe:
        return base64.urlsafe_b64encode(s).decode('utf-8')

    return base64.b64encode(s).decode('utf-8')


def decode(s):
    """
    Base64 decode.

    :param s:
    :return: str
    """
    if isinstance(s, str):
        if len(s) % 4 > 0:
            s = s + '=' * (4 - len(s) % 4)
        s = s.encode('utf-8')

    # URL Safe
    s = s.translate(bytes.maketrans(b'-_', b'+/'))

    try:
        return base64.b64decode(s).decode('utf-8')
    except UnicodeDecodeError:
        return base64.b64decode(s)
