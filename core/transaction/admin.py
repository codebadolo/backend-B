from django.contrib import admin
from .models import Wallet, Transaction, Currency

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'currency')
    search_fields = ('user__username', 'balance')
    list_filter = ('currency',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'amount', 'transaction_type', 'timestamp', 'status')
    list_filter = ('transaction_type', 'status',)  # Filtering by type and status
    
    # This separates deposits, sends, and withdrawals in the admin
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Add logic to show separate transaction types
        if 'deposits' in request.GET:
            return qs.filter(transaction_type='deposit')
        return qs

    # Adding a custom view for deposits
    def changelist_view(self, request, extra_context=None):
        extra_context = {'show_deposits': True}  # Add any extra context here
        return super(TransactionAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol', 'exchange_rate_to_usd')
    search_fields = ('name', 'code')

admin.site.register(Transaction, TransactionAdmin)