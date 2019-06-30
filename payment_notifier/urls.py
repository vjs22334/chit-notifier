from django.urls import path
from .views import *

urlpatterns = [

    path('home/',home ),
    path('sendWhatsApp/',sendWhatsapp ),
    path('WhatsAppReport/',WhatsAppReport ),
    path('sendWhatsAppMessages/',SendWhatsappMessages ),

]