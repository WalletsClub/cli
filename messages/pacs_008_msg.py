# -*- coding:utf-8 -*-

import json
import random
from datetime import datetime
from string import Template
import logging

try:
    logging.getLogger('faker').setLevel(logging.FATAL)
    from faker import Faker
except Exception as e:
    pass

from identifier import make_instruction_identification, make_biz_message_identification, make_e2e_identification
from money import Money


def template():
    """ pacs.008 message template """
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
            "MsgDefIdr": "pacs.008.001.09",
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
            "FIToFICstmrCdtTrf": {
                "GrpHdr": {
                    "MsgId": "${Doc_MsgId}",
                    "CreDtTm": "${Doc_CreDtTm}",
                    "IntrBkSttlmDt": "${Doc_IntrBkSttlmDt}",
                    "NbOfTxs": "1",
                    "TtlIntrBkSttlmAmt": {
                        "Ccy": "${Doc_TtlIntrBkSttlmAmt_Ccy}",
                        "Amount": '${Doc_TtlIntrBkSttlmAmt_Amount}'
                    },
                    "SttlmInf": {
                        "SttlmMtd": "CLRG",
                        "ClrSys": {
                            "Cd": "WNET"
                        }
                    }
                },
                "CdtTrfTxInf": {
                    "PmtId": {
                        "InstrId": "${Doc_PmtId_InstrId}",
                        "EndToEndId": "${Doc_PmtId_EndToEndId}",
                        "TxId": "${Doc_PmtId_TxId}"
                    },
                    "PmtTpInf": {
                        "SvcLvl": {
                            "Cd": "SDVA"
                        },
                        "LclInstrm": {
                            "Prtry": "${Doc_Prtry}"
                        }
                    },
                    "IntrBkSttlmAmt": {
                        "Ccy": "${Doc_IntrBkSttlmAmt_Ccy}",
                        "Amount": "${Doc_IntrBkSttlmAmt_Amount}"
                    },
                    "ChrgBr": "SLEV",
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
                    "Dbtr": {
                        "Nm": "${Doc_Dbtr_Nm}"
                    },
                    "DbtrAcct": {
                        "Id": {
                            "Othr": {
                                "Id": "${Doc_DbtrAcct_Id}"
                            }
                        }
                    },
                    "DbtrAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Doc_DbtrAgt_MmbId}"
                            }
                        }
                    },
                    "CdtrAgt": {
                        "FinInstnId": {
                            "ClrSysMmbId": {
                                "MmbId": "${Doc_CdtrAgt_MmbId}"
                            }
                        }
                    },
                    "Cdtr": {
                        "Nm": "${Doc_Cdtr_Nm}"
                    },
                    "CdtrAcct": {
                        "Id": {
                            "Othr": {
                                "Id": "${Doc_CdtrAcct_Id}"
                            }
                        }
                    },
                    "RmtInf": {
                        "Ustrd": "${Doc_RmtInf_Ustrd}",
                        "Strd": {
                            "RfrdDocInf": {
                                "Nb": "${Doc_RmtInf_Strd_RfrdDocInf_Nb}",
                                "RltdDt": "${Doc_RmtInf_Strd_RfrdDocInf_RltdDt}",
                            }

                        }
                    },
                    "RgltryRptg": [
                        {
                            "DbtCdtRptgInd": "DEBT",
                            "Authrty": {
                                "Nm": "Joke",
                                "Ctry": "HK"
                            },
                            "Dtls": [
                                {
                                    "Tp": "NZEF",
                                    "Dt": "2021-05-27",
                                    "Ctry": "HK",
                                    "Cd": "WHUQX",
                                    "Amt": "1024.18",
                                    "Inf": ["Additional details", "More details"]
                                }
                            ]
                        }
                    ]
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


def bake(debtor_pid, net_pid, creditor_pid, ccy='HKD'):
    """ Bake a pacs.008 message """

    hdr_biz_msg_id = make_biz_message_identification(debtor_pid)
    doc_msg_id = make_instruction_identification(debtor_pid)
    doc_e2e_msg_id = make_e2e_identification(debtor_pid)
    # random 1 ~ 100 amount
    money = Money(round(random.uniform(1, 10), 2), ccy)

    fake = Faker()

    kwargs = {
        'AppHdr_BizMsgIdr': hdr_biz_msg_id,
        'AppHdr_CreDt': str(datetime.now().strftime('%Y-%m-%d')),
        'AppHdr_Fr_MmbId': debtor_pid,
        'AppHdr_To_MmbId': net_pid,
        'Doc_MsgId': doc_msg_id,
        'Doc_IntrBkSttlmDt': str(datetime.now().strftime('%Y-%m-%d')),
        'Doc_TtlIntrBkSttlmAmt_Ccy': money.currency.code,
        'Doc_CreDtTm': str(datetime.now().astimezone(None).isoformat()),
        'Doc_TtlIntrBkSttlmAmt_Amount': str(money.amount),
        'Doc_PmtId_InstrId': doc_e2e_msg_id,
        'Doc_PmtId_EndToEndId': doc_e2e_msg_id,
        'Doc_PmtId_TxId': doc_e2e_msg_id,
        'Doc_Prtry': 'BUSINESS',
        'Doc_IntrBkSttlmAmt_Ccy': money.currency.code,
        'Doc_IntrBkSttlmAmt_Amount': str(money.amount),
        'Doc_InstgAgt_MmbId': debtor_pid,
        'Doc_InstdAgt_MmbId': creditor_pid,
        'Doc_Dbtr_Nm': fake.name(),
        'Doc_DbtrAcct_Id': fake.md5(),
        'Doc_DbtrAgt_MmbId': debtor_pid,
        'Doc_CdtrAgt_MmbId': creditor_pid,
        'Doc_Cdtr_Nm': fake.name(),
        'Doc_CdtrAcct_Id': fake.md5(),
        'Doc_RmtInf_Ustrd': fake.free_email(),
        'Doc_RmtInf_Strd_RfrdDocInf_Nb': fake.iban(),
        'Doc_RmtInf_Strd_RfrdDocInf_RltdDt': fake.date(pattern='%Y-%m-%d'),
    }

    message = build(**kwargs)

    return message
