from django.test import TestCase
from rest_framework import status

from api.models import Account, Transaction, AuthToken

from rest_framework.test import APIRequestFactory, APITestCase


# factory = APIRequestFactory()
# request = factory.post('/accounts', {'currency': 'EUR', 'balance': 5000}, format='json')

class BaseAccountTest(APITestCase):
    url = '/api/v1/accounts'
    currency = ['EUR', 'USD', 'GBR', 'CHF']

    def setUp(self):
        self.auth_token = AuthToken.objects.create()
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_token.token)


class AccountTests(BaseAccountTest):
    def test_create_account_positive_eur(self):
        """use correct data for account creations"""
        data = {'currency': 'EUR'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, 'EUR')

    def test_create_account_positive_usd(self):
        """use correct data for account creations"""
        data = {'currency': 'USD'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, 'USD')

    def test_create_account_positive_gbr(self):
        """use correct data for account creations"""
        data = {'currency': 'GBR'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, 'GBR')

    def test_create_account_positive_chf(self):
        """use correct data for account creations"""
        data = {'currency': 'CHF'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, 'CHF')

    def test_create_account_negative_currency(self):
        """use incorrect currency data for account creations"""
        data = {'currency': 'FFF'}
        response = self.client.post(path=self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.get().currency, 'CHF')
#
# class TransactionTests(APITestCase):
#     def setUp(self):
#         self.auth_token = AuthToken.objects.create()
#         self.sourceAccount = Account.objects.create(balance=10000,
#                                                     currency='USD')
#
#     def test_default_transaction(self):
#         """ It means we have data for both accounts, sourceAccount and destAccount also"""
#         url = '/api/v1/transactions'
#         data = {'sourceAccount'}
