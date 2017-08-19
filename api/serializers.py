from decimal import Decimal
from rest_framework import serializers
from api.constants import CHF, GBP, EUR, USD
from api.models import Account, Transaction
from core.exceptions import CustomValidationError


class AccountSerializer(serializers.ModelSerializer):
    currency = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        model = Account
        fields = ('identifier', 'currency', 'balance')

    def validate(self, attrs):
        if not self.initial_data.get('currency'):
            raise CustomValidationError(detail={'message': '"currency" is required field',
                                                'error': 'true'})
        if self.initial_data.get('currency') not in [USD, EUR, GBP, CHF]:
            raise CustomValidationError(detail={'message': '"currency" should be one of "USD", "EUR", "GBR" or "CHF"',
                                                'error': 'true'})
        if self.initial_data.get('balance') and self.initial_data.get('balance') < 0:
            raise CustomValidationError(detail={'message': 'negative balance on any account are not permitted.',
                                                'error': 'true'})

        return super().validate(attrs)

    def create(self, attrs):
        account = Account.objects.create(currency=attrs.get('currency'),
                                         balance=attrs.get('balance'))
        return account


class TransactionSerializer(serializers.ModelSerializer):
    sourceAccount = serializers.CharField(max_length=8, required=False)
    destAccount = serializers.CharField(max_length=8, required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        model = Transaction
        fields = ('sourceAccount', 'destAccount', 'amount', 'id')

    def validate(self, attrs):
        source = self.initial_data.get('sourceAccount')
        dest = self.initial_data.get('destAccount')
        amount = self.initial_data.get('amount')
        if amount < 0:
            raise CustomValidationError(detail={'message': 'amount can\'t be less then 0',
                                                'error': 'true'})
        if not source and not dest:
            raise CustomValidationError(detail={'message': '"sourceAccount" and "destAccount" are not specified',
                                                'error': 'true'})
        if source == dest:
            raise CustomValidationError(detail={'message': '"sourceAccount" and "destAccount" numbers are identical',
                                                'error': 'true'})
        if source and len(source) < 8 or dest and len(dest) < 8:
            raise CustomValidationError(
                detail={'message': '"sourceAccount" or "destAccount" contain less than 8 digits',
                        'error': 'true'})
        if not Account.objects.filter(identifier=source).first() and source:
            raise CustomValidationError(detail={'message': 'wrong number of sourceAccount',
                                                'error': 'true'})
        if not Account.objects.filter(identifier=dest).first() and dest:
            raise CustomValidationError(detail={'message': 'wrong number of destAccount',
                                                'error': 'true'})
        if Account.objects.filter(identifier=dest).first() and \
                        len(str(Account.objects.filter(identifier=dest).first().balance + Decimal(amount))) > 10:
            raise CustomValidationError(detail={'message': 'the amount  is too lage for that account balance'})

        return super().validate(attrs)


class AccountDetailsSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=8)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=5)

    class Meta:
        model = Account
        fields = '__all__'
