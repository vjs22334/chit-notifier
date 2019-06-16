from django.contrib import admin
from payment_notifier.models import *
# Register your models here.



class userDetailsAdmin(admin.ModelAdmin):
    search_fields = ('name','sms_number','whatsapp_number','email')

admin.site.register(userDetails,userDetailsAdmin)
