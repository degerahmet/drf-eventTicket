from django.db import models
from place.models import Place, SeatingPlan

import string
import random

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

    def __str__(self):
        return f'{self.title} | {self.place} | {self.date} | {self.duration}'

class TicketLevel(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='ticket_price')
    seat = models.OneToOneField(SeatingPlan,on_delete=models.CASCADE,related_name='plan')
    price = models.FloatField()

    def __str__(self):
        return f'{self.event} | ${self.price}'

class EventSeat(models.Model):
    level = models.ForeignKey(TicketLevel,on_delete=models.CASCADE,related_name='level')
    code = models.CharField(max_length=7)

    def __str__(self):
        return f'{self.level.seat.code} {self.code} | ${self.level}'

##### SEATS CREATING SECTION AFTER SEATING PLAN SAVE
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=TicketLevel)
def create_seat(sender, instance, **kwargs):
    capacity = instance.seat.capacity


    for x in range(capacity):
        letters = string.ascii_uppercase
        seat_code = ''.join(random.choice(letters) for i in range(7))
        seat = EventSeat(level=instance, code=seat_code)
        seat.save()


class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    detail = models.OneToOneField(EventSeat,on_delete=models.CASCADE,related_name='detail')

    def __str__(self):
        return f'{self.user} | {self.detail.seat}'


