# -*- coding: utf-8 -*-

from time import time


def uniqid():
    """ Returns a short and unique identifier using the hex of the current timestamp. """
    return hex(int(time()*10000000))[2:]
