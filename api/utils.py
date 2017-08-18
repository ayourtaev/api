from random import randint


def get_account_identifier():
    return '%0.8d' % randint(0, 99999999)

