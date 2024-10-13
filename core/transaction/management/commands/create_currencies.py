from django.core.management.base import BaseCommand
from transaction.models import Currency  # Make sure this is the correct import path

class Command(BaseCommand):
    help = 'Creates 20 of the most used currencies in Africa and the world'

    def handle(self, *args, **kwargs):
        # List of currencies
        currencies = [
            {"name": "US Dollar", "code": "USD", "symbol": "$", "exchange_rate_to_usd": 1.00},
            {"name": "Euro", "code": "EUR", "symbol": "€", "exchange_rate_to_usd": 0.85},
            {"name": "British Pound", "code": "GBP", "symbol": "£", "exchange_rate_to_usd": 0.75},
            {"name": "Nigerian Naira", "code": "NGN", "symbol": "₦", "exchange_rate_to_usd": 410.50},
            {"name": "South African Rand", "code": "ZAR", "symbol": "R", "exchange_rate_to_usd": 14.50},
            {"name": "Kenyan Shilling", "code": "KES", "symbol": "KSh", "exchange_rate_to_usd": 108.50},
            {"name": "Ghanaian Cedi", "code": "GHS", "symbol": "₵", "exchange_rate_to_usd": 6.10},
            {"name": "Egyptian Pound", "code": "EGP", "symbol": "£", "exchange_rate_to_usd": 15.70},
            {"name": "Moroccan Dirham", "code": "MAD", "symbol": "د.م.", "exchange_rate_to_usd": 9.00},
            {"name": "Tunisian Dinar", "code": "TND", "symbol": "د.ت", "exchange_rate_to_usd": 2.85},
            {"name": "CFA Franc BEAC", "code": "XAF", "symbol": "FCFA", "exchange_rate_to_usd": 552.50},
            {"name": "CFA Franc BCEAO", "code": "XOF", "symbol": "CFA", "exchange_rate_to_usd": 552.50},
            {"name": "Ethiopian Birr", "code": "ETB", "symbol": "Br", "exchange_rate_to_usd": 44.50},
            {"name": "Ugandan Shilling", "code": "UGX", "symbol": "USh", "exchange_rate_to_usd": 3650.00},
            {"name": "Algerian Dinar", "code": "DZD", "symbol": "دج", "exchange_rate_to_usd": 135.00},
            {"name": "Botswana Pula", "code": "BWP", "symbol": "P", "exchange_rate_to_usd": 11.00},
            {"name": "Tanzanian Shilling", "code": "TZS", "symbol": "TSh", "exchange_rate_to_usd": 2315.00},
            {"name": "Zambian Kwacha", "code": "ZMW", "symbol": "ZK", "exchange_rate_to_usd": 22.50},
            {"name": "Congolese Franc", "code": "CDF", "symbol": "FC", "exchange_rate_to_usd": 2000.00},
            {"name": "Mozambican Metical", "code": "MZN", "symbol": "MT", "exchange_rate_to_usd": 63.00},
        ]

        # Iterate over the currencies and create or update them in the database
        for currency_data in currencies:
            currency, created = Currency.objects.update_or_create(
                code=currency_data['code'],
                defaults={
                    'name': currency_data['name'],
                    'symbol': currency_data['symbol'],
                    'exchange_rate_to_usd': currency_data['exchange_rate_to_usd'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created {currency.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Successfully updated {currency.name}"))
