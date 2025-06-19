from django.contrib import admin
from .models import Mailing, Message, MailingTrying


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("first_mailing", "frequency", "status", "next_mailing", "is_immediate", )
    search_fields = ("status", "clients", "message", "next_mailing",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("topic", "content", )


@admin.register(MailingTrying)
class MailingTryingAdmin(admin.ModelAdmin):
    list_display = ("last_mailing", "status_trying", "server_response", "mailing", )

