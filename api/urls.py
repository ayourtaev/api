from django.conf.urls import url

from api.views import (
    AccountTransactions,
    ListOfAccounts,
    AccountDetailInformation, AccountCreateView, TransactionsCreateView)

urlpatterns = [
    url(r'^list_of_accounts', ListOfAccounts.as_view()),
    url(r'^account_transactions/(?P<pk>\d{8})', AccountTransactions.as_view(), name='account_transactions'),
    url(r'^account_details/(?P<pk>\d{8})', AccountDetailInformation.as_view()),
    url(r'^accounts', AccountCreateView.as_view()),
    url(r'^transactions', TransactionsCreateView.as_view())

]
