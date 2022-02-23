from django.db import models
from place.models import Place, Seat, SeatingPlan

from users.models import User
# Create your models here.



class Event(models.Model):
    EVENT_TYPES = [
        ('N','NBA'),
        ('F','NFL'),
        ('C','CONCERT'),
        ('D','DONATION'),
        ('F','FESTIVAL'),
        ('B','BASKETBALL'),
        ('S','SOCCER'),
    ]
    title = models.CharField(max_length=255)
    place = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='event')
    event_type = models.CharField(choices=EVENT_TYPES,max_length=1)
    date = models.DateTimeField()
    duration = models.IntegerField()

class TicketPrice(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='ticket_price')
    seat = models.OneToOneField(Seat,on_delete=models.CASCADE,related_name='seat')
    price = models.FloatField()


class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    detail = models.OneToOneField(TicketPrice,on_delete=models.CASCADE,related_name='detail')


