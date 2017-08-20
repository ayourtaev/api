from uuid import uuid4
from django.db import models

from api.constants import DECLINED, COMPLETED, CREATED, GBP, EUR, USD, CHF
from api.utils import get_account_identifier


class Account(models.Model):
    CURRENCY_CHOICES = (
        (USD, USD),
        (EUR, EUR),
        (GBP, GBP),
        (CHF, CHF),
    )

    identifier = models.CharField(max_length=8, primary_key=True, default=get_account_identifier)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default=USD)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return 'identifier: {identifier}, balance: {balance}, currency: {currency}'.format(
            identifier=self.identifier, balance=self.balance, currency=self.currency
        )


class Transaction(models.Model):
    TRANSACTION_STATES = (
        (COMPLETED, COMPLETED),
        (DECLINED, DECLINED),
        (CREATED, CREATED)
    )
    id = models.CharField(max_length=8, primary_key=True, default=get_account_identifier)
    sourceAccount = models.ForeignKey('api.Account', related_name='sourceAccount', blank=True, null=True)
    destAccount = models.ForeignKey('api.Account', related_name='destAccount', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    state = models.CharField(max_length=10, choices=TRANSACTION_STATES, default=CREATED)
    reason = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return 'sourceAccount: {sourceAccount}, destAccount: {destAccount}, amount: {amount}'.format(
            sourceAccount=self.sourceAccount.identifier, destAccount=self.destAccount.identifier, amount=self.amount
        )


class AuthToken(models.Model):
    token = models.CharField(max_length=20, default=uuid4().hex)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
