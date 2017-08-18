from django.db import models
from api.utils import get_account_identifier


class Account(models.Model):
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBR', 'GBR'),
        ('CHF', 'CHF'),
    )

    identifier = models.CharField(max_length=8, primary_key=True, default=get_account_identifier)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='USD')

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return 'identifier: {identifier}, balance: {balance}, currency: {currency}'.format(
            identifier=self.identifier, balance=self.balance, currency=self.currency
        )


class Transaction(models.Model):
    source = models.ForeignKey('api.Account', related_name='source')
    destination = models.ForeignKey('api.Account', related_name='destination')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return 'source: {source}, destination: {destination}, amount: {amount}'.format(
            source=self.source.identifier, destination=self.destination.identifier, amount=self.amount
        )