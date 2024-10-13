from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            # Create a new profile only if it doesn't exist
            Profile.objects.get_or_create(user=instance)
        else:
            instance.profile.save()

    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.username} - {self.balance}'

    # Add funds to the wallet
    def deposit(self, amount):
        self.balance += amount
        self.save()

    # Remove funds from the wallet
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient funds")
        
        
class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], default='PENDING')

    def __str__(self):
        return f'Transaction from {self.sender.username} to {self.receiver.username} for {self.amount}'
        
        

        