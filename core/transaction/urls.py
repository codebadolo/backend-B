from django.urls import path
from .views import  (
    DepositView, WithdrawView, SendMoneyView 
    ,TransactionListView  , UserTransactionListView , 
    PreviewTransferFeeView, CurrencyListView ,MyTransactionsView) 

urlpatterns = [
    path('transaction/deposit/', DepositView.as_view(), name='transaction-deposit'),
    path('transaction/withdraw/', WithdrawView.as_view(), name='transaction-withdraw'),
    path('transaction/send/', SendMoneyView.as_view(), name='transaction-send'),
    path('transaction/my-transactions/<int:user_id>/', MyTransactionsView.as_view(), name='my-transactions'),
    path('transaction/transactions/', TransactionListView.as_view(), name='transaction-list'),
  
    path('transaction/my-transactions/', MyTransactionsView.as_view(), name='my-transactions'),
    path('transaction/my-transactions/<int:user_id>/', MyTransactionsView.as_view(), name='user-transactions'),
    
    path('currencies/', CurrencyListView.as_view(), name='currency-list'),
    path('transaction/preview-fee/', PreviewTransferFeeView.as_view(), name='preview-transfer-fee'),
]
