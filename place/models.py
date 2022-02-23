from random import choice
from django.db import models
import string
import random
# Create your models here.



class Place(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    capacity = models.IntegerField()


class SeatingPlan(models.Model):
    LEVELS = [
        (0,'Ground'),
        (1,'Level 1'),
        (2,'Level 2'),
        (3,'Level 3'),
        (4,'Level 4'),
        (5,'Level 5'),
        (6,'VIP'),
    ]
    place = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='seatingPlan')
    capacity = models.IntegerField()
    code = models.CharField(max_length=255)
    level = models.IntegerField(choices=LEVELS)


    def save(self):
        capacity = self.capacity


        for x in range(capacity):

            letters = string.ascii_uppercase
            seat_code = ''.join(random.choice(letters) for i in range(7))
            seat = Seat(SeatingPlan=self.id,seat_code=seat_code)
            
            seat.save()
        
        return super().save()


class Seat(models.Model):
    seating_plan = models.ForeignKey(SeatingPlan,on_delete=models.CASCADE,related_name='seat')
    seat_code = models.CharField(max_length=7)