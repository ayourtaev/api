from django.conf.urls import url

from api.views import (
    AccountTransactions,
    ListOfAccounts
)

urlpatterns = [
    url(r'^list_of_accounts', ListOfAccounts.as_view()),
    url(r'^account_detalis/(?P<pk>\d{8})', AccountTransactions.as_view(), name='account_detail'),
]
