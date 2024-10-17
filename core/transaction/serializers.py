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
    username = serializers.CharField(write_only=True, required=False)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = ['amount', 'currency', 'username']

    def create(self, validated_data):
        # Get the username from the validated data, default to the request's user if not provided
        username = validated_data.get('username', self.context['request'].user.username)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with username '{username}' does not exist.")
        
        currency = validated_data.get('currency')
        amount = validated_data['amount']

        wallet = Wallet.objects.get(user=user)
        wallet.deposit(amount, currency)

        return Transaction.objects.create(
            sender=user,
            amount=amount,
            transaction_type='deposit',
            currency=currency,
            status='COMPLETED'
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
    phone_number = serializers.CharField(write_only=True, required=True)  # Accept phone number instead of receiver

    class Meta:
        model = Transaction
        fields = ['phone_number', 'amount', 'currency']

    def create(self, validated_data):
        sender = self.context['request'].user
        phone_number = validated_data.get('phone_number')
        
        # Look up the receiver based on the phone number
        try:
            receiver = User.objects.get(profile__phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"No user found with phone number '{phone_number}'.")

        amount = validated_data['amount']
        currency = validated_data['currency']

        sender_wallet = Wallet.objects.get(user=sender)
        receiver_wallet = Wallet.objects.get(user=receiver)

        if sender_wallet.balance >= amount:
            sender_wallet.withdraw(amount)
            receiver_wallet.deposit(amount, currency)
            return Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                transaction_type='send',
                currency=currency,
                status='COMPLETED'
            )
        else:
            raise serializers.ValidationError("Insufficient balance.")