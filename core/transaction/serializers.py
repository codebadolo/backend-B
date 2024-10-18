from rest_framework import serializers
from .models import Wallet, Transaction, Currency
from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import authenticate
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
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Transaction
        fields = ['username', 'email', 'password', 'amount']

    def validate(self, data):
        # Extract the username, email, and password from the validated data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            # Check if the user with the given username exists
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with the specified username does not exist.")

        # Authenticate using the email and password
        if not authenticate(username=username, password=password) or user.email != email:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data

    def create(self, validated_data):
        # Get the authenticated user and amount to withdraw
        user = validated_data['user']
        amount = validated_data['amount']

        # Perform the withdrawal operation
        wallet = Wallet.objects.get(user=user)
        wallet.withdraw(amount)

        # Create the transaction record
        return Transaction.objects.create(
            sender=user,
            amount=amount,
            transaction_type='withdraw',
            status='COMPLETED'
        )
        
class SendMoneySerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=True)  # Receiver identified by phone number
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())  # Sender's currency

    class Meta:
        model = Transaction
        fields = ['phone_number', 'amount', 'currency']

    def calculate_transfer_fee(self, amount):
        # Example: A fee of 2% of the transaction amount
        fee_percentage = Decimal('0.02')
        return amount * fee_percentage

    def create(self, validated_data):
        sender = self.context['request'].user
        phone_number = validated_data.get('phone_number')
        
        # Look up the receiver based on the phone number
        try:
            receiver = User.objects.get(profile__phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"No user found with phone number '{phone_number}'.")

        amount = validated_data['amount']
        sender_currency = validated_data['currency']
        
        # Fetch the sender's and receiver's wallets
        sender_wallet = Wallet.objects.get(user=sender)
        receiver_wallet = Wallet.objects.get(user=receiver)
        receiver_currency = receiver_wallet.currency

        # Calculate the fee
        transfer_fee = self.calculate_transfer_fee(amount)

        # Calculate the total amount to deduct (amount + fee)
        total_deduction = amount + transfer_fee

        # Convert amount from sender's currency to receiver's currency
        conversion_rate = sender_currency.exchange_rate_to_usd / receiver_currency.exchange_rate_to_usd
        converted_amount = amount * conversion_rate

        if sender_wallet.balance >= total_deduction:
            # Deduct the amount + fee from the sender and convert it to the receiver's currency
            sender_wallet.withdraw(total_deduction)
            receiver_wallet.deposit(converted_amount, receiver_currency)

            # Create and return the transaction
            return Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=converted_amount,
                fee=transfer_fee,
                transaction_type='send',
                currency=receiver_currency,
                status='COMPLETED'
            )
        else:
            raise serializers.ValidationError("Insufficient balance.")
        
class PreviewTransferFeeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    def validate(self, data):
        # Validate receiver exists
        phone_number = data.get('phone_number')
        try:
            User.objects.get(profile__phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"No user found with phone number '{phone_number}'.")
        
        return data

    def calculate_transfer_fee(self, amount):
        # Example fee rate: 2%
        fee_percentage = Decimal('0.02')
        return amount * fee_percentage

    def get_fee_preview(self, sender, amount, currency):
        fee = self.calculate_transfer_fee(amount)
        total_deduction = amount + fee
        return {
            "amount": amount,
            "fee": fee,
            "total_deduction": total_deduction,
            "currency": currency.code,
        }
        
        