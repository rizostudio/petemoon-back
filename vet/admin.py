from django.contrib import admin

from .models import ReserveTimes, VetComment, Visit

admin.site.register(ReserveTimes)
admin.site.register(VetComment)
admin.site.register(Visit)