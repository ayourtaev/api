from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase

from api.constants import DECLINED, CHF, GBR, USD, EUR
from api.models import Account, AuthToken, Transaction


class BaseTest(APITestCase):
    currency = [EUR, USD, GBR, CHF]

    def setUp(self):
        self.auth_token = AuthToken.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_token.token)


class BaseAccountTest(BaseTest):
    url = '/api/v1/accounts'


class BaseTransactionTest(BaseTest):
    url = '/api/v1/transactions'


class AuthTokenTests(APITestCase):
    url = '/api/v1/accounts'

    def test_with_auth_token(self):
        self.auth_token = AuthToken.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_token.token)
        response = self.client.post(path=self.url, data={'currency': CHF}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_without_auth_token(self):
        response = self.client.post(path=self.url, data={'currency': CHF}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AccountTests(BaseAccountTest):
    def test_create_account_positive_eur(self):
        """use correct data for account creations"""
        data = {'currency': EUR}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, EUR)

    def test_create_account_positive_usd(self):
        """use correct data for account creations"""
        data = {'currency': USD}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, USD)

    def test_create_account_positive_gbr(self):
        """use correct data for account creations"""
        data = {'currency': GBR}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, GBR)

    def test_create_account_positive_chf(self):
        """use correct data for account creations"""
        data = {'currency': CHF}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, CHF)

    def test_create_account_negative_currency(self):
        """use incorrect currency data for account creations"""
        data = {'currency': 'FFF'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data.get('message'), '"currency" should be one of "USD", "EUR", "GBR" or "CHF"')

    def test_create_account_negavite_without_currency(self):
        """currency field is required"""
        data = {}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_positive_balance(self):
        """use correct data for account creations"""
        data = {'currency': USD, 'balance': 5000}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().balance, 5000)

    def test_create_account_negative_balance_less(self):
        """negative balance on any account are not permitted."""
        data = {'currency': USD, 'balance': -5000}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data.get('message'), 'negative balance on any account are not permitted.')

    def test_create_account_negative_balance_great(self):
        """balance can't be more then 9999999999"""
        data = {'currency': USD, 'balance': 99999999999}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TransactionExternalTests(BaseTransactionTest):
    """Transactions with only a destination account are called deposits, t
        ransactions with only a source account are called withdrawals."""

    def test_withdraw_below_zero(self):
        self.sourceAccount = Account.objects.create(currency='USD')

        data = {'sourceAccount': self.sourceAccount.identifier,
                'amount': 50000}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['transaction_state'], DECLINED)

    def test_withdraw_positive(self):
        self.sourceAccount = Account.objects.create(currency='USD', balance='50000')

        data = {'sourceAccount': self.sourceAccount.identifier,
                'amount': 777}
        before = self.sourceAccount.balance
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().balance, Decimal(before) - Decimal(data['amount']))

    def test_deposit_positive(self):
        self.destAccount = Account.objects.create(currency='USD', balance='50000')

        data = {'destAccount': self.destAccount.identifier,
                'amount': 777}
        before = self.destAccount.balance
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().balance, Decimal(before) + Decimal(data['amount']))

    def test_deposit_over_limit(self):
        self.destAccount = Account.objects.create(currency='USD', balance='9999999.00')

        data = {'destAccount': self.destAccount.identifier,
                'amount': 99999999.99}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

class TransactionInternalTests(BaseTransactionTest):
    """Internal transfers convert the transferred amount if the source
    and destination accounts are denominated in different currencies."""

