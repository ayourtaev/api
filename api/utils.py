from fixerio import Fixerio
from random import randint


def get_account_identifier():
    return '%0.8d' % randint(0, 99999999)


def calc_currency(currency, amount):
    fxrio = Fixerio(symbols=[currency])
    response = fxrio.latest()
    summ_amount = amount * response['rates'][currency]
    return summ_amount
