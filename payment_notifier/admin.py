from django.contrib import admin
from payment_notifier.models import *
# Register your models here.



class userDetailsAdmin(admin.ModelAdmin):
    search_fields = ('name','sms_number','whatsapp_number','email')


class MessageAdmin(admin.ModelAdmin):
    search_fields = ('message_type','message_text')


class WhatsappMessagesToSendAdmin(admin.ModelAdmin):
    search_fields = ('name','status','group')

class WhatsAppLogsAdmin(admin.ModelAdmin):
    search_fields = ('name','status','group','logged_date')

admin.site.register(userDetails,userDetailsAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(WhatsAppLogs,WhatsAppLogsAdmin)
admin.site.register(WhatsappMessagesToSend,WhatsappMessagesToSendAdmin)
