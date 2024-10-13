from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)  # Example: 'USD', 'EUR'
    symbol = models.CharField(max_length=5)
    exchange_rate_to_usd = models.DecimalField(max_digits=10, decimal_places=4, default=1.00)
    last_updated = models.DateTimeField(null=True, blank=True)  # Track when the rate was updated

    def __str__(self):
        return f'{self.name} ({self.code})'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)  # Preferred currency

    def deposit(self, amount, deposit_currency):
        # Convert amount to user's preferred currency using the exchange rate
        exchange_rate = deposit_currency.exchange_rate_to_usd / self.currency.exchange_rate_to_usd
        converted_amount = Decimal(amount) * Decimal(exchange_rate)
        self.balance += converted_amount
        self.save()

    def withdraw(self, amount):
        if Decimal(amount) <= self.balance:
            self.balance -= Decimal(amount)
            self.save()
        else:
            raise ValueError("Insufficient funds")
        
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('send', 'Send'),
        ('withdraw', 'Withdraw'),
    )

    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='deposit')

    def __str__(self):
        return f'Transaction {self.transaction_type} of {self.amount} from {self.sender} to {self.receiver}'
