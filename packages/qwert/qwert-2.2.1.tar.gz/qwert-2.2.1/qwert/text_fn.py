#!/usr/bin/env python
# encoding: utf-8


def gram_align_right(s, line_width: int = 20):
    """
    Format for telegram, align right.

    :param s: input text
    :param int line_width: Width
    :return: str
    """
    return '`{}`'.format(str(s).rjust(line_width))
