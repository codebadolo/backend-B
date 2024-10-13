from rest_framework import serializers
from .models import Wallet, Transaction, Currency
from django.contrib.auth.models import User
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'code', 'symbol', 'exchange_rate_to_usd']

class WalletSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Wallet
        fields = ['balance', 'currency']

class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # Display the sender's username
    receiver = serializers.StringRelatedField()  # Display the receiver's username
    currency = serializers.StringRelatedField()  # Display the currency code instead of ID

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'transaction_type', 'currency', 'status', 'timestamp']
        read_only_fields = ['id', 'status', 'timestamp']

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']

    def create(self, validated_data):
        user = self.context['request'].user
        return Transaction.objects.create(
            user=user,
            amount=validated_data['amount'],
            transaction_type='deposit'
        )

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']

    def create(self, validated_data):
        user = self.context['request'].user
        return Transaction.objects.create(
            user=user,
            amount=validated_data['amount'],
            transaction_type='withdraw'
        )

class SendMoneySerializer(serializers.ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ['receiver', 'amount']

    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = validated_data['receiver']
        amount = validated_data['amount']
        return Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            transaction_type='send'
        )
