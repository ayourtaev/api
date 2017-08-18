from django.db.models import Q
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from api.models import Account, Transaction


class AccountTransactions(generics.RetrieveAPIView):
    template_name = 'account_transactions.html'
    queryset = Transaction.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(Q(source_id=kwargs['pk']) | Q(destination_id=kwargs['pk']))
        return Response({'list_of_transactions': transactions})


class ListOfAccounts(generics.ListAPIView):
    template_name = 'list_of_accounts.html'
    renderer_classes = (TemplateHTMLRenderer,)
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        return Response({'list_of_accounts': self.get_queryset()})
