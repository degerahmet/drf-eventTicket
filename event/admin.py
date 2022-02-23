from django.contrib import admin
from .models import Event,TicketPrice,Ticket
# Register your models here.

admin.site.register(Event)
admin.site.register(TicketPrice)
admin.site.register(Ticket)