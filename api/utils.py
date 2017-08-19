from fixerio import Fixerio
from random import randint
from decimal import Decimal


def get_account_identifier():
    return '%0.8d' % randint(0, 99999999)


def calc_currency(currency, amount):
    fxrio = Fixerio(symbols=[currency])
    response = fxrio.latest()
    if currency == response.get('base'):
        return Decimal(amount)
    summ_amount = Decimal(amount) * Decimal(response['rates'][currency])
    return summ_amount.quantize(Decimal('1.00'))
