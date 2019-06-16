from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

phoneNumberValidator = RegexValidator(regex=r'^\d{10}$')

class userDetails(models.Model):
    
    name = models.CharField(max_length = 50,unique=True)
    whatsapp_number = models.CharField(max_length = 15,blank = True, validators = [phoneNumberValidator])
    sms_number = models.CharField(max_length = 15,blank = True, validators = [phoneNumberValidator])
    email = models.EmailField(blank = True)

    class Meta:
        verbose_name = 'User Details'
        verbose_name_plural = "User Details"

    def __str__(self):
        return self.name