from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
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
        
class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="api_key")
    key = models.CharField(max_length=100, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4()).replace("-", "")        
    
    
@receiver(post_save, sender=User)
def create_user_api_key(sender, instance, created, **kwargs):
    if created:
        APIKey.objects.create(user=instance)    