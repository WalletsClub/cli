# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification


def template():
    """ pacs.002 message template """

    tpl = {
        "AppHdr": {
            "BizMsgIdr": "${AppHdr_BizMsgIdr}",
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
            "MsgDefIdr": "pacs.002.001.11",
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
            "FIToFIPmtStsRpt": {
                "GrpHdr": {
                    "MsgId": "${Doc_MsgId}",
                    "CreDtTm": "${Doc_CreDtTm}"
                },
                "OrgnlGrpInfAndSts": {
                    "OrgnlCreDtTm": "${Doc_OrgnlCreDtTm}",
                    "OrgnlMsgId": "${Doc_OrgnlMsgId}",
                    "OrgnlMsgNmId": "pacs.008.001.09",
                    "OrgnlNbOfTxs": 1
                },
                "TxInfAndSts": {
                    "AccptncDtTm": "${Doc_AccptncDtTm}",
                    "InstgAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Doc_InstgAgt_MmbId}"
                            }
                        }
                    },
                    "InstdAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Doc_InstdAgt_MmbId}"
                            }
                        }
                    },
                    "OrgnlInstrId": "${Doc_OrgnlInstrId}",
                    "TxSts": "${Doc_TxSts}"
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


def bake(my_pid, net_pid):
    """ Bake a pacs.002 message """

    hdr_biz_msg_id = make_biz_message_identification(my_pid)
    doc_msg_id = make_instruction_identification(my_pid)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_pid,
        'AppHdr_To_MmbId': net_pid,
        'Doc_MsgId': doc_msg_id,
        'Doc_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'Doc_OrgnlCreDtTm': '',
        'Doc_OrgnlMsgId': '',
        'Doc_AccptncDtTm': str(datetime.now().astimezone(None).isoformat()),
        'Doc_InstdAgt_MmbId': '',
        'Doc_InstgAgt_MmbId': '',
        'Doc_OrgnlInstrId': '',
        'Doc_TxSts': ''
    }

    message = build(**kwargs)

    return message
