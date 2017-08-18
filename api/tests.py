from django.test import TestCase
from api.models import Account, Transaction

class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(balance=100000.12)
        Account.objects.create(balance=100000.32)

    def test_first_test(self):
        all = Account.objects.all()
        for _ in all:
            print(_)


