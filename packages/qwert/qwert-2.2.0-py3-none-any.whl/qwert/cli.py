#!/usr/bin/env python
# encoding: utf-8
import cli_print as cp
import re
import decimal


def confirm(s: str = ''):
    """
    Ask yes/no, retry if invalid.

    :param str s: prompt
    :return: bool
    """
    while True:
        value = input('> {} [y/n]: '.format(s)).lower()
        if value:
            if value in 'yesrtui':
                return True
            elif value in 'novbm,':
                return False


def raw(s: str = '', preset: str = None):
    """
    Get input, retry if empty.

    :param str s: prompt
    :param str preset: preset value
    :return: str
    """
    if preset and confirm('Use {} = "{}":'.format(s, preset)):
        return preset

    while True:
        value = input('> {}: '.format(s))
        if value:
            return value


def integer(s: str = '', preset: int = None):
    """
    Get a integer, retry if empty or ValueError.

    :param str s: prompt
    :param int preset: preset value
    :return: int
    """
    if preset and confirm('Use {} = {}:'.format(s, preset)):
        return preset

    return __integer(s)


def __integer(s: str = ''):
    """
    Get a integer, retry if empty or ValueError.

    :param str s: prompt
    :return: int
    """
    value = None
    try:
        while True:
            value = raw(s)
            return int(value)
    except ValueError:
        print('"{}" is not a integer.'.format(value))
        return __integer(s)


def dec(s: str = '', preset: int or decimal.Decimal or str = None):
    """
    Get a decimal, retry if empty or ValueError.

    :param str s: prompt
    :param int ore decimal.Decimal or str preset: preset value
    :return: int
    """
    try:
        if preset and confirm('Use {} = {}:'.format(s, decimal.Decimal(preset))):
            return preset
        return __dec(s)
    except decimal.InvalidOperation:
        print('"{}" is not a decimal.'.format(preset))
        return __dec(s)


def __dec(s: str = ''):
    """
    Get a decimal, retry if empty or ValueError.

    :param str s: prompt
    :return: int
    """
    value = None
    try:
        while True:
            value = raw(s)
            return decimal.Decimal(value)
    except decimal.InvalidOperation:
        print('"{}" is not a decimal.'.format(value))
        return __dec(s)


def str_hex(s: str, case_sensitive: bool = False):
    """
    Get a hex, retry if empty or not hex.

    :param str s: prompt
    :param bool case_sensitive: case_sensitive
    :return: str
    """
    pattern = r'^[0-9a-fA-F]+$'

    while True:
        r = raw(s)
        if r.lower() == 'none':
            return None
        else:
            if not case_sensitive:
                r = r.lower()

            if re.match(pattern, r):
                return r
            else:
                print('must be hex')


def pause(s: str = 'press any key to continue'):
    """
    Pause with a prompt.

    :param str s: prompt
    :return: None
    """
    _ = input('# {}: '.format(s))
    return


def copy(value: str, force: bool = False, key: str = None):
    """
    Copy to clip.

    :param str value: value to be copied
    :param bool force: without a prompt pause
    :param str key: tip
    :return: None
    """
    import cli_print as cp
    import pyperclip

    if not force:
        if key:
            pause('Press any key to copy {} '.format(key)
                  + cp.Fore.LIGHTCYAN_EX + str(value)
                  + cp.Style.RESET_ALL + ' to clip')
        else:
            pause('Press any key to copy '
                  + cp.Fore.LIGHTCYAN_EX + str(value)
                  + cp.Style.RESET_ALL + ' to clip')

        cp.wr('\x1b[1A\x1b[2K')  # remove the prompt line.
        cp.fi()
    if key:
        cp.about_t('Copy {}'.format(key), value, 'to clip')
    else:
        cp.about_t('Copy', value, 'to clip')
    pyperclip.copy(value)
    cp.success()
    return


def __print_sleep(i: int, t: int):
    """
    Function for `sleep`.

    :param int i: current
    :param int t: amount
    :return: None
    """
    if t < 90:
        cp.wr(cp.Fore.LIGHTBLUE_EX + ' - [' + '>' * i + '-' * (t - i) + '] sleep {}/{} s\r'.format(i, t))
        cp.fx()
    else:
        cp.wr(cp.Fore.LIGHTBLUE_EX + ' - sleep {}/{} s\r'.format(i, t))
        cp.fx()
    return


def sleep(t: int = None, b: int = None):
    """
    Sleep for a while.

    :param int t: Min seconds
    :param int b: Max seconds
    :return:
    """
    import time
    import random

    if t and b:
        t = random.randint(t, b)
    elif t is None:
        t = random.randint(10, 60)

    __print_sleep(0, t)

    for i in range(1, t + 1):
        time.sleep(1)
        cp.previous_line(True)
        __print_sleep(i, t)

    return t
