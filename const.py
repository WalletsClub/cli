# -*- coding:utf-8 -*-

import sys
import logging
from logging import handlers

conf = './setting.json'
dummy_cp_pid = 'ZRMTHKHHXXX'  # todo 改成统一模拟对手方

log = logging.getLogger()
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

fh = handlers.RotatingFileHandler('/tmp/walletsnet.log', maxBytes=(1048576 * 5), backupCount=7)
fh.setFormatter(format)
log.addHandler(fh)
