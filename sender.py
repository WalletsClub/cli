# -*- coding:utf-8 -*-

import json

import requests

from jws import serialize_compact
from const import conf, log
from participant import get
from util import s, f


class Sender(object):
    """ Message sender """

    def __init__(self, participant):
        self.participant = participant

    def post(self, message):
        """ POST message to WalletsNet """

        scheme = message['AppHdr']['MsgDefIdr'][:8]
        walletsnet = get(conf, 'NET')

        payload = json.dumps(message)
        request_body = serialize_compact(payload, self.participant.private_key, self.participant.kid)
        response = requests.post(walletsnet.api, data=request_body, timeout=5)

        if response.status_code == 200:
            log.info(s('{0} --> WalletsNet: {1} message send successful!'.format(self.participant.name, scheme)))
        else:
            log.info(f(' {0} --> WalletsNet: {1} message send fail'.format(self.participant.name, scheme)))

        return response
