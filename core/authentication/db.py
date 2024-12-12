from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
# Profile Model
# 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # KYC fields
    kyc_document_type = models.CharField(max_length=50, blank=True, choices=(
        ('PASSPORT', 'Passport'),
        ('ID_CARD', 'ID Card'),
        ('DRIVERS_LICENSE', 'Driver’s License'),
    ))
    kyc_document_image = models.ImageField(upload_to='kyc_documents/', null=True, blank=True)
    kyc_status = models.CharField(max_length=50, default='PENDING', choices=(
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ))

    def __str__(self):
        return self.user.username
# Signal to create/update Profile automatically when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new profile only if it doesn't exist
        Profile.objects.get_or_create(user=instance)
    else:
        instance.profile.save()    

# Currency Model
class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)  # Example: 'USD', 'EUR'
    symbol = models.CharField(max_length=5)
    exchange_rate_to_usd = models.DecimalField(max_digits=10, decimal_places=4, default=1.00)
    last_updated = models.DateTimeField(null=True, blank=True)  # Track when the rate was updated

    def __str__(self):
        return f'{self.name} ({self.code})'

# Wallet Model
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
        
    def get_balance(self, balance):
        pass     

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('send', 'Send'),
        ('withdraw', 'Withdraw'),
    )

    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)  # Transaction currency
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, default='deposit')
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    def __str__(self):
        return f'Transaction {self.transaction_type} of {self.amount} from {self.sender} to {self.receiver}'
