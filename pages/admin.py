from django.contrib import admin

from pages.models import ContactUser

@admin.register(ContactUser)
class ContactUser(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'message', 'created_at',]
