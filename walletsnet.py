# -*- coding:utf-8 -*-

import os
import json
import time
import datetime
import logging
from ipaddress import ip_address

import requests
import emoji
import webbrowser
import fire
from pyfiglet import Figlet
from termcolor import colored
from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException
from rfc3339 import rfc3339

from jws import deserialize_compact
from participant import get
from const import conf, log
from util import s, f, w
from participant import dummy
from sender import Sender

app = Flask('transceiver')
app.config['ENV'] = 'development'
app.logger.setLevel(logging.DEBUG)


@app.errorhandler(HTTPException)
def handle_bad_request(e):
    return 'Bad request!', 400


@app.before_request
def start_timer():
    """ Start timer """
    g.start = time.time()


@app.after_request
def log_request(response):
    """ Log after request """
    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    if request.method == 'POST':
        args = request.get_data(as_text=True)
    elif request.method == 'GET':
        args = dict(request.args)
    else:
        args = {}

    log_params = [
        ('method', request.method, 'red'),
        ('path', request.path, 'red'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'white'),
        ('params', args, 'white')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colored("{}={}".format(name, value), color=color)
        parts.append(part)
    line = " ".join(parts)

    app.logger.debug(line)

    return response


@app.route('/', methods=['POST'])
def index():
    try:
        return jsonify(message="I am working :)")
    except Exception as e:
        log.critical('Oops! Exception occurred.')
        import traceback
        log.critical(traceback.format_exc())
        return jsonify(resultCode="F")


@app.route('/inbox', methods=['POST'])
def inbox():
    """ Receive message from WalletsNet """
    try:
        request_body = request.get_data()

        walletsnet = get(conf, 'NET')
        received_message = json.loads(deserialize_compact(request_body, walletsnet.public_key).payload)

        if os.environ.get('forward_to') is not None:
            requests.post(os.environ.get('forward_to'), data=received_message)

        return jsonify(resultCode="T")
    except Exception as e:
        log.critical('Oops! Exception occurred.')
        import traceback
        log.critical(traceback.format_exc())
        return jsonify(resultCode="F")


@app.route('/outbox', methods=['POST'])
def outbox():
    """ Send message to WalletsNet """
    try:
        request_body = request.get_data()

        return jsonify(resultCode="T")
    except Exception as e:
        log.critical('Oops! Exception occurred.')
        log.critical(e)
        return jsonify(resultCode="F")


class CommandLine(object):
    """ WalletsNet command line tool """

    def __init__(self):
        if not os.path.exists(conf):
            raise SystemExit((colored('Missing configure file: {0}'.format(conf), color='red')))

    def version(self):
        """ version """
        print('0.1.0')

    def listen(self, host='0.0.0.0', port=12222, forward_to=None, log_level='DEBUG'):
        """  Communicate with WalletsNet on your local machine, do not use it in production deployment """

        if ip_address(host).is_private:
            raise SystemExit((colored('Public IP address expected: {0}'.format(host), color='red')))

        f = Figlet(font="banner3-d", width=1000)
        log.info('\n\n' + colored(f.renderText('WalletsNet.'), color='white') +
                 colored('\n * WARNING: This is a development server. Do not use it in a production deployment.\n',
                         color='red'))

        if forward_to != '' and forward_to is not None:
            os.environ["forward_to"] = forward_to

        if log_level:
            app.logger.setLevel(logging.getLevelName(log_level))

        app.run(host=host, port=port, use_reloader=True, debug=True, ssl_context='adhoc')

    def check(self):
        """ Check if everything ok """
        # todo 在portal上加个api支持这个功能
        print('Result of checklist:\n')
        print(s('Participant ID'))
        print(s('Webhook'))
        print(w('Public key'))
        print(f('Connection'))
        print('\n')

    def examples(self, action='list'):
        """ A list of available samples that can be created and bootstrapped by the CLI  """
        if action == 'list':
            print('List of available samples:\n')

            print('1. Credit transfer')
            print('Command: walletsnet trigger --example="credit transfer"')
            print('Blog: Learn how to make a credit transfer instruction')
            print(emoji.emojize(":backhand_index_pointing_right: ") + 'https://blog.walletsclub.com/credit_transfer')

            print('\n')

            print('2. Request to Pay')
            print('Command: walletsnet trigger --example="request to pay"')
            print('Blog: Learn how to make a request to pay instruction')
            print(emoji.emojize(":backhand_index_pointing_right: ") + 'https://blog.walletsclub.com/request_to_pay')

            print('\n')

    def __trigger_pacs_008(self):
        """ trigger send credit transfer message to WalletsNet """
        from messages.pacs_008_msg import bake

        walletsnet = get(conf, 'NET')
        me = get(conf, 'ME')

        pacs_008_message = bake(me.pid, walletsnet.pid, dummy.pid)

        sender = Sender(me)
        response = sender.post(pacs_008_message)

        return response

    def __trigger_pain_013(self):
        """ trigger send Request to Pay message to WalletsNet """
        from messages.pain_013_msg import bake

        walletsnet = get(conf, 'NET')
        me = get(conf, 'ME')

        pain_013_message = bake(me.pid, walletsnet.pid, dummy.pid)

        sender = Sender(me)
        response = sender.post(pain_013_message)

        return response

    def __trigger_admi_011(self):
        """ trigger send ECHO message to WalletsNet """
        from messages.admi_011_msg import bake

        walletsnet = get(conf, 'NET')
        me = get(conf, 'ME')

        admi_011_message = bake(me.pid, walletsnet.pid)

        sender = Sender(me)
        response = sender.post(admi_011_message)

        return response

    def trigger(self, example='echo'):
        """ Trigger example instructions to conduct local testing. """

        if example.lower() == 'echo':
            response = self.__trigger_admi_011()
        elif example.lower() == 'credit transfer':
            response = self.__trigger_pacs_008()
        elif example.lower() == 'request to pay':
            response = self.__trigger_pain_013()
        else:
            print(f('Invalid example'))
            return

        if response.status_code == 200:
            print(s('Trigger succeeded! Check dashboard for transaction details.'))
        else:
            print(s('Trigger failed! Response: {0}'.format(response.text)))

    def open(self, topic):
        """ Open WalletsNet page """
        if topic == 'dashboard':
            webbrowser.open('http://portal.walletsclub.com', new=2)
        elif topic == 'doc':
            webbrowser.open('https://walletsclub.com/Documentation', new=2)
        else:
            webbrowser.open('http://www.walletsclub.com', new=2)

    def status(self):
        """ Return WalletsNet system status and service availability. """
        from datetime import datetime
        from util import border

        response = self.__trigger_admi_011()

        as_of = 'As of: {0}'.format(datetime.now().astimezone(None).isoformat())

        if response.status_code == 200:
            prefix = colored('[Online]', 'green')
            print(border(prefix + ' WalletsNet is online.' + '\n' + as_of))
        else:
            prefix = colored('[Under Maintenance]', 'yellow')
            print(border(prefix + ' WalletsNet is under maintenance.' + '\n' + as_of))

    def help(self, topic=None):
        """ Help guide """
        if topic is None:
            print('Check out our blog ' +
                  emoji.emojize(":backhand_index_pointing_right: ") +
                  'https://blog.walletsclub.com')
            return

        if topic.lower() == 'connection':
            print('Blog: Learn how to make a connection ' +
                  emoji.emojize(":backhand_index_pointing_right: ") +
                  'https://blog.walletsclub.com/connection')
        else:
            pass


def cli():
    fire.Fire(CommandLine)
