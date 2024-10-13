from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from transaction.models import Transaction

class Command(BaseCommand):
    help = 'Create two users and perform a transaction between them.'

    def handle(self, *args, **kwargs):
        # Create two users
        user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password123')
        user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password123')

        self.stdout.write(self.style.SUCCESS(f"Created user1 with ID {user1.id}"))
        self.stdout.write(self.style.SUCCESS(f"Created user2 with ID {user2.id}"))

        # Perform a transaction between user1 and user2
        transaction = Transaction.objects.create(
            sender=user1,
            receiver=user2,
            amount=100.0,
            currency='USD'
        )

        self.stdout.write(self.style.SUCCESS(f"Transaction of {transaction.amount} {transaction.currency} from {user1.username} to {user2.username} created successfully."))
