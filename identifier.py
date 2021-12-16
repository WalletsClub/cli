# -*- coding:utf-8 -*-

import random


def rand_x_digit_num(x, leading_zeroes=True):
    """Return an X digit number, leading_zeroes returns a string, otherwise int"""
    if not leading_zeroes:
        # wrap with str() for uniform results
        return random.randint(10 ** (x - 1), 10 ** x - 1)
    else:
        if x > 6000:
            return ''.join([str(random.randint(0, 9)) for i in range(x)])
        else:
            return '{0:0{x}d}'.format(random.randint(0, 10 ** x - 1), x=x)


def make_biz_message_identification(participant_id):
    """ Generate message id, structure: BYYYYMMDDbbbbbbbbbbbXAAAnnnnnnnnnnn """
    from datetime import datetime

    date = datetime.now().strftime('%Y%m%d')
    serial_identifier = 'PSP'
    source = 'B'
    serial_nunmber = rand_x_digit_num(11)

    mid = "B{date}{participant_id}{source}{serial_identifier}{serial_nunmber}" \
        .format(date=date,
                participant_id=participant_id,
                source=source,
                serial_identifier=serial_identifier,
                serial_nunmber=serial_nunmber)

    return mid


def make_message_identification(participant_id):
    """ Generate message id, structure: MYYYYMMDDbbbbbbbbbbbXAAAnnnnnnnnnnn """
    from datetime import datetime

    date = datetime.now().strftime('%Y%m%d')
    serial_identifier = 'PSP'
    source = 'B'
    serial_nunmber = rand_x_digit_num(11)

    mid = "M{date}{participant_id}{source}{serial_identifier}{serial_nunmber}" \
        .format(date=date,
                participant_id=participant_id,
                source=source,
                serial_identifier=serial_identifier,
                serial_nunmber=serial_nunmber)

    return mid


def make_instruction_identification(participant_id):
    """ Generate instruction id, structure: YYYYMMDDbbbbbbbbbbbBRRRRnnnnnnnnnnnn """
    from datetime import datetime

    date = datetime.now().strftime('%Y%m%d')
    serial_identifier = 'WPSP'
    source = 'B'
    serial_nunmber = rand_x_digit_num(11)

    iid = "{date}{participant_id}{source}{serial_identifier}{serial_nunmber}" \
        .format(date=date,
                participant_id=participant_id,
                source=source,
                serial_identifier=serial_identifier,
                serial_nunmber=serial_nunmber)

    return iid


def make_inner_identification(participant_id):
    """ Generate inner order id, structure: YYYYMMDDbbbbbbbbbbbBRRRRnnnnnnnnnnnn """
    from datetime import datetime

    date = datetime.now().strftime('%Y%m%d')
    serial_identifier = 'WPSP'
    source = 'A'
    serial_nunmber = rand_x_digit_num(11)

    iid = "{date}{participant_id}{source}{serial_identifier}{serial_nunmber}" \
        .format(date=date,
                participant_id=participant_id,
                source=source,
                serial_identifier=serial_identifier,
                serial_nunmber=serial_nunmber)

    return iid


# alias
make_transaction_identification = make_instruction_identification
make_e2e_identification = make_instruction_identification
make_agreement_identification = make_inner_identification
