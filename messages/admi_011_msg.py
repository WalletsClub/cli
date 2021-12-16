# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification


def template():
    """ admi.011 message template """
    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
            "MsgDefIdr": "admi.011.001.01",
            "CreDt": "${AppHdr_CreDt}",
            "Fr": {
                "FIId": {
                    "FinInstnId": {
                        "ClrSysMmbId": {
                            "MmbId": "${AppHdr_Fr_MmbId}"
                        }
                    }
                }
            },
            "To": {
                "FIId": {
                    "FinInstnId": {
                        "ClrSysMmbId": {
                            "MmbId": "${AppHdr_To_MmbId}"
                        }
                    }
                }
            }
        },
        "Document": {
            "SysEvtAck": {
                "MsgId": "${Document_MsgId}",
                "AckDtls": {
                    "EvtCd": "${Document_EvtCd}"
                }
            }
        }
    }

    return json.dumps(tpl)


def build(**kwargs):
    """ build message, return dict """
    t = Template(template())
    content = t.substitute(**kwargs)

    return json.loads(content)


def bake(pid, net_pid):
    """ Bake a admi.011 message """

    hdr_biz_msg_id = make_biz_message_identification(pid)
    doc_msg_id = make_instruction_identification(pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': pid,
        'AppHdr_To_MmbId': net_pid,
        'Document_MsgId': doc_msg_id,
        'Document_EvtCd': 'ECHO',
    }

    message = build(**kwargs)

    return message
