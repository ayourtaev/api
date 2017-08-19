from decimal import Decimal

from django.db.models import Q

from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from api.constants import DECLINED, COMPLETED
from api.models import Account, Transaction
from api.permissions import AuthTokenKeeper
from api.serializers import AccountDetailsSerializer, AccountSerializer, TransactionSerializer
from api.utils import calc_currency


# UI

class AccountTransactions(generics.RetrieveAPIView):
    template_name = 'account_transactions.html'
    queryset = Transaction.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(Q(sourceAccount=kwargs['pk']) | Q(destAccount=kwargs['pk']))
        return Response({'list_of_transactions': transactions})


class ListOfAccounts(generics.ListAPIView):
    template_name = 'list_of_accounts.html'
    renderer_classes = (TemplateHTMLRenderer,)
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({'list_of_accounts': self.get_queryset()})


# API

class AccountCreateView(CreateAPIView):
    model = Account
    permission_classes = (AuthTokenKeeper,)
    serializer_class = AccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data={'data': {'accountNumber': serializer.data.get('identifier')}, 'error': 'false'},
            status=HTTP_201_CREATED,
            headers=headers
        )


class TransactionsCreateView(CreateAPIView):
    model = Transaction
    permission_classes = (AuthTokenKeeper,)
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        source = Account.objects.filter(identifier=serializer.validated_data.get('sourceAccount')).first()
        dest = Account.objects.filter(identifier=serializer.validated_data.get('destAccount')).first()
        amount = Decimal(serializer.validated_data.get('amount'))

        if source and dest:
            if source.currency != dest.currency:
                source_calc = calc_currency(source.currency, amount)
                dest_calc = calc_currency(dest.currency, amount)
                if source.balance - source_calc < 0:
                    return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount,
                                                      state=DECLINED)
                else:
                    source.balance -= source_calc
                    source.save()
                    dest.balance += dest_calc
                    dest.save()
                    return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount,
                                                      state=DECLINED)
            else:
                if source.balance - amount < 0:
                    return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount,
                                                      state=DECLINED)
                else:
                    source.balance -= amount
                    dest.balance += amount
                    source.save()
                    dest.save()
                    return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount,
                                                      state=COMPLETED)

        if not source:
            dest.balance += amount
            dest.save()
            return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount,
                                              state=COMPLETED)
        if not dest:
            if source.balance - amount < 0:
                return Transaction.objects.create(sourceAccount=source, destAccount=dest, amount=amount, state=DECLINED)
            else:
                source.balance -= amount
                source.save()
                return Transaction.objects.create(sourceAccount=source, amount=amount,
                                                  state=COMPLETED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data={'data': {'transactionNumber': transaction.id, 'transaction_state': transaction.state},
                  'error': 'false'},
            status=HTTP_201_CREATED,
            headers=headers
        )


# Custom API

class AccountDetailInformation(APIView):
    permission_classes = (AuthTokenKeeper,)
    queryset = Account.objects.all()

    def get(self, requet, *args, **kwargs):
        responsed_data = Account.objects.get(identifier=kwargs['pk'])
        serializer = AccountDetailsSerializer(responsed_data)
        return Response(serializer.data)
