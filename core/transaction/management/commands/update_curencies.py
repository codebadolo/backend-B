import requests
from django.core.management.base import BaseCommand
from transaction.models import Currency
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Updates currency exchange rates from Fixer.io or any external API'

    def handle(self, *args, **kwargs):
        # Replace this URL with the actual API call you're using (Fixer.io, CurrencyLayer, etc.)
        api_url = 'http://data.fixer.io/api/latest?access_key=YOUR_API_KEY&base=USD'

        response = requests.get(api_url)
        data = response.json()

        if data.get('success'):
            rates = data.get('rates')
            for currency_code, rate in rates.items():
                # Update the exchange rate in your database
                try:
                    currency = Currency.objects.get(code=currency_code)
                    currency.exchange_rate_to_usd = rate
                    currency.last_updated = now()
                    currency.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated {currency.name} rate"))
                except Currency.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Currency {currency_code} does not exist in the database"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch rates: {data.get('error')}"))
