# -*- coding:utf-8 -*-

import json
from datetime import datetime
from string import Template

from identifier import make_biz_message_identification, make_instruction_identification
from zremit.config import my_participant_id, nt_participant_id


def template():
    """ pacs.002消息模板, 返回一个字符串 """
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
    """ 通过模板构建消息体, 返回一个dict """
    t = Template(template())
    content = t.substitute(**kwargs)

    return json.loads(content)


def bake():
    """ 生成一个完整的&正确的默认消息 """
    my_participant_mem_id = my_participant_id
    walletsnet_id = nt_participant_id

    hdr_biz_msg_id = make_biz_message_identification(my_participant_mem_id)
    doc_msg_id = make_instruction_identification(my_participant_mem_id)

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': my_participant_mem_id,
        'AppHdr_To_MmbId': walletsnet_id,
        'Doc_MsgId': doc_msg_id,
        'Doc_CreDtTm': str(datetime.now().astimezone(None).isoformat()),  # 标准要求是一个ISO8601的时间
        'Doc_OrgnlCreDtTm': '',
        'Doc_OrgnlMsgId': '',
        'Doc_AccptncDtTm': str(datetime.now().astimezone(None).isoformat()),  # 标准要求是一个ISO8601的时间,
        'Doc_InstdAgt_MmbId': '',
        'Doc_InstgAgt_MmbId': '',
        'Doc_OrgnlInstrId': '',
        'Doc_TxSts': ''
    }

    message = build(**kwargs)

    # print(message)

    return message
