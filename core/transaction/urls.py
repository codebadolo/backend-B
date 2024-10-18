from django.urls import path
from .views import  (
    DepositView, WithdrawView, SendMoneyView 
    ,TransactionListView  , UserTransactionListView , PreviewTransferFeeView, CurrencyListView) 

urlpatterns = [
     path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('send/', SendMoneyView.as_view(), name='send-money'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactionsperuser/', UserTransactionListView.as_view(), name='user-transactions'),
     path('currencies/', CurrencyListView.as_view(), name='currency-list'),
     path('transaction/preview-fee/', PreviewTransferFeeView.as_view(), name='preview-transfer-fee'),
]
