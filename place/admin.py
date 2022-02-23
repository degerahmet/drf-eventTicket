from django.contrib import admin
from .models import Seat,SeatingPlan,Place

# Register your models here.


admin.site.register(SeatingPlan)
admin.site.register(Seat)
admin.site.register(Place)