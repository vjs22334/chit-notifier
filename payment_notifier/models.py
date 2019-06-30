from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

phoneNumberValidator = RegexValidator(regex=r'^\d{10}$')


message_types = (
    ("1","whatsapp"),
    ("2","email"),
    ("3","sms")
)

status = (
    ("1","name not present"),
    ("2","file not present"),
    ("3","no. not in contacts"),
    ("4","queued"),
    ("5","success"),

)

class userDetails(models.Model):
    
    name = models.CharField(max_length = 50,unique=True)
    whatsapp_number = models.CharField(max_length = 15,blank = True, null=True, validators = [phoneNumberValidator])
    sms_number = models.CharField(max_length = 15,blank = True, null = True, validators = [phoneNumberValidator])
    email = models.EmailField(blank = True)

    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = "User Details"

    def __str__(self):
        return self.name


class Message(models.Model):
    message_type = models.CharField(max_length = 50,choices = message_types,default = "1" )
    message_text = models.TextField(blank = True,null = True) 



class WhatsappMessagesToSend(models.Model):
    name = models.CharField(max_length = 50)
    status = models.CharField(max_length = 20,choices = status)
    path = models.CharField(max_length = 200)
    group = models.CharField(max_length = 50)
    
    def __str__(self):
        return ':'.join((self.name,self.get_status_display(),self.group))

class WhatsAppLogs(models.Model):
    name = models.CharField(max_length = 50)
    logged_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length = 20,choices = status)
    group = models.CharField(max_length = 50)

    def __str__(self):
        return '  :  '.join((self.name,self.get_status_display(),self.group,self.logged_date.strftime("%m/%d/%Y, %H:%M:%S")))




