from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Transaction, Wallet , Currency
from .serializers import (
DepositSerializer,TransactionSerializer , SendMoneySerializer, WithdrawSerializer ,CurrencySerializer )
from rest_framework.permissions import IsAuthenticated 

class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
# Deposit View
class DepositView(generics.CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        wallet = Wallet.objects.get(user=self.request.user)
        serializer.save(user=self.request.user)
        # Perform the deposit by increasing the user's wallet balance
        wallet.deposit(serializer.validated_data['amount'])

# Withdraw View
class WithdrawView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        wallet = Wallet.objects.get(user=self.request.user)
        serializer.save(user=self.request.user)
        # Perform the withdrawal by decreasing the user's wallet balance
        wallet.withdraw(serializer.validated_data['amount'])

# Send Money View
class SendMoneyView(generics.CreateAPIView):
    serializer_class = SendMoneySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data['receiver']
        amount = serializer.validated_data['amount']
        sender_wallet = Wallet.objects.get(user=sender)
        receiver_wallet = Wallet.objects.get(user=receiver)
        
        # Check if the sender has enough balance to send
        if sender_wallet.balance >= amount:
            sender_wallet.withdraw(amount)
            receiver_wallet.deposit(amount)
            serializer.save(sender=sender, receiver=receiver)
        else:
            raise serializers.ValidationError("Insufficient balance.")

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer  # Explicitly defining the serializer class
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        transaction_type = self.request.query_params.get('transaction_type')
        if transaction_type:
            return Transaction.objects.filter(sender=self.request.user, transaction_type=transaction_type) | Transaction.objects.filter(receiver=self.request.user, transaction_type=transaction_type)
        return Transaction.objects.filter(sender=self.request.user) | Transaction.objects.filter(receiver=self.request.user)
class UserTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions for the current authenticated user (either as sender or receiver)
        user = self.request.user
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)