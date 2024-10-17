from django.urls import path
from .views import  (
    DepositView, WithdrawView, SendMoneyView  ,TransactionListView  , UserTransactionListView) 

urlpatterns = [
     path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('send/', SendMoneyView.as_view(), name='send-money'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactionsperuser/', UserTransactionListView.as_view(), name='user-transactions'),
    
]
