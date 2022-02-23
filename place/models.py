from django.db import models
# Create your models here.



class Place(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f'{self.name}  -  {self.city}'


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


    def __str__(self):
        return f'{self.place.name}  |  CODE : {self.code}  | {self.get_level_display()}'


