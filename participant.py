# -*- coding:utf-8 -*-

import os
import json
from functools import lru_cache
from const import dummy_cp_pid


class Participant(object):
    """ Participant """

    def __init__(self, **kwargs):
        self.api = kwargs.get('api')
        self.pid = kwargs.get('pid')
        self.kid = kwargs.get('kid')
        self.public_key = kwargs.get('public_key')
        self.private_key = kwargs.get('private_key')

    def __hash__(self):
        return hash(self.pid)

    @property
    def name(self):
        return self.pid[:4]


@lru_cache
def get(conf, role='NET'):
    """ Get wallentnet participant entity from conf file """

    if not os.path.exists(conf):
        raise FileNotFoundError('No configure file found: {0}'.format(conf))

    with open(conf, 'r') as f:
        setting = json.load(f)

    if role == 'NET':
        return Participant(api=setting['walletsnet']['api'],
                           pid=setting['walletsnet']['pid'],
                           public_key=setting['walletsnet']['public_key'])
    elif role == 'ME':
        return Participant(api=setting['my']['api'],
                           pid=setting['my']['pid'],
                           kid=setting['my']['kid'],
                           private_key=setting['my']['private_key'])
    else:
        raise ValueError('Role should be "NET" of "ME"')


# dummy count-party participant
dummy = Participant(pid=dummy_cp_pid)
