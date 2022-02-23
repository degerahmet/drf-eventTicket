from django.contrib import admin
from .models import Event,TicketLevel,Ticket
# Register your models here.

admin.site.register(Event)
admin.site.register(TicketLevel)
admin.site.register(Ticket)