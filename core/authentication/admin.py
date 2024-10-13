from django.contrib import admin
from .models import Profile
from django.utils.html import format_html
from unfold.admin import ModelAdmin
@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('profile_image_tag' , 'user', 'kyc_status', 'kyc_document_type', 'country', 'city')
    search_fields = ('user__username', 'user__email', 'kyc_status')
    #list_filter = ('kyc_status', 'kyc_document_type', 'country')
    readonly_fields = ('kyc_status',)

    # Show these fields in the form to add/edit a profile
    def kyc_document_image_preview(self, obj):
        if obj.kyc_document_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.kyc_document_image.url)
        return "No Image"
    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_image.url)
        return "No Image"

    kyc_document_image_preview.short_description = "KYC Document Preview"
    profile_image_tag.short_description = 'Profile Image'

    fieldsets = (
        (None, {
            'fields': ('user', 'profile_image', 'country', 'city', 'address', 'phone_number', 'date_of_birth')
        }),
        ('KYC Information', {
            'fields': ('kyc_document_type', 'kyc_document_image', 'kyc_document_image_preview', 'kyc_status'),
        }),
    )
    readonly_fields = ['kyc_document_image_preview', 'kyc_status']