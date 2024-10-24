from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Transaction, Wallet , Currency
from rest_framework.views import APIView
from .serializers import (
DepositSerializer,TransactionSerializer , 
SendMoneySerializer, WithdrawSerializer ,

CurrencySerializer ,PreviewTransferFeeSerializer )
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.models import User
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
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve `user_id` from query params or use current user
        user_id = self.request.query_params.get('user_id', self.request.user.id)
        try:
            user = User.objects.get(id=user_id)
            transaction_type = self.request.query_params.get('transaction_type')
            if transaction_type:
                return Transaction.objects.filter(sender=user, transaction_type=transaction_type) | Transaction.objects.filter(receiver=user, transaction_type=transaction_type)
            return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
        except User.DoesNotExist:
            return Transaction.objects.none()
        
class UserTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter transactions for the current authenticated user (either as sender or receiver)
        user = self.request.user
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
    
    

class PreviewTransferFeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PreviewTransferFeeSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user
            amount = serializer.validated_data['amount']
            currency = serializer.validated_data['currency']
            
            fee_details = serializer.get_fee_preview(sender, amount, currency)
            return Response(fee_details)
        return Response(serializer.errors, status=400)    
    
class MyTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve user_id from the URL, if provided
        user_id = self.kwargs.get('user_id')

        try:
            # If user_id is provided, fetch transactions for that user
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                # Default to authenticated user if no user_id is provided
                user = self.request.user

            # Return all transactions where the user is either the sender or receiver
            return Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)
        except User.DoesNotExist:
            return Transaction.objects.none()

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        # Check if the user exists
        if user_id:
            try:
                User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return super().list(request, *args, **kwargs)
