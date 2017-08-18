from rest_framework import serializers
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from api.models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    currency = serializers.CharField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        model = Account
        fields = ('identifier', 'currency', 'balance')

    def validate(self, attrs):
        if not self.initial_data.get('currency'):
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={'message': '"currency" is required field',
                                                      'error': 'true'})
        if self.initial_data.get('currency') not in ['USD', 'EUR', 'GBR', 'CHF']:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={
                                                  'message': '"currency" should be one of "USD", "EUR", "GBR" or "CHF"',
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
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={'message': 'amount can\'t be less then 0',
                                                      'error': 'true'})
        if not source and not dest:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={'message': '"sourceAccount" and "destAccount" are not specified',
                                                      'error': 'true'})
        if source == dest:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={
                                                  'message': '"sourceAccount" and "destAccount" numbers are identical',
                                                  'error': 'true'})
        if source and len(source) < 8 or dest and len(dest) < 8:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={
                                                  'message': '"sourceAccount" or "destAccount" contain less than 8 characters',
                                                  'error': 'true'})
        if not Account.objects.filter(
                identifier=source).first() and source:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={
                                                  'message': 'wrong number of sourceAccount',
                                                  'error': 'true'})
        if not Account.objects.filter(
                identifier=dest).first() and dest:
            raise serializers.ValidationError(code=HTTP_422_UNPROCESSABLE_ENTITY,
                                              detail={
                                                  'message': 'wrong number of destAccount',
                                                  'error': 'true'})

        return super().validate(attrs)

        # def create(self, attrs):
        #     transaction = Transaction.objects.create(
        #         sourceAccount=Account.objects.get(identifier=attrs.get('sourceAccount')),
        #         destAccount=Account.objects.get(identifier=attrs.get('destAccount')),
        #         amount=attrs.get('amount'))
        #     return transaction


#
# class TypeOfTransactionSerializer(serializers.Serializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'
#
#     def validate(self, attrs):
#         transaction = Transaction.objects.get(id=attrs.get('id'))
#         if source


class AccountDetailsSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=8)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=5)

    class Meta:
        model = Account
        fields = '__all__'
