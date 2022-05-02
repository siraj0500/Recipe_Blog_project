from django.contrib import admin
from .models import User_Message


class UsermessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'sender_message')


admin.site.register(User_Message, UsermessageAdmin)
