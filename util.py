# -*- coding:utf-8 -*-

import json

from prettytable import PrettyTable
from tabulate import tabulate
from termcolor import colored


def table(d):
    """ Print dict as table view """
    try:
        x = PrettyTable()
        x.field_names = d.keys()
        x.add_row(d.values())
        return x
    except:
        return d


def j(d):
    """ Print dict as json view """
    try:
        d.pop('_id', None)

        return json.dumps(d, indent=4, default=str, ensure_ascii=False)
    except:
        return d


def s(text):
    """ return success text """
    try:
        return colored('[√] ', 'green') + text
    except:
        return text


def f(text):
    """ return fail text """
    try:
        return colored('[×] ', 'red') + text
    except:
        return text


def w(text):
    """ return warning text """
    try:
        return colored('[!] ', 'yellow') + text
    except:
        return text


def border(text):
    """ Print text with border """
    try:
        tb = [[text]]
        output = tabulate(tb, tablefmt='grid')
        return output
    except:
        return text
