from django.contrib import admin
from .models import ReserveTimes, VetComment, Visit


admin.site.register(ReserveTimes)
admin.site.register(VetComment)

class VisitAdmin(admin.ModelAdmin):
    list_display = ('visit_id', 'vet', 'user')
    readonly_fields = ('price',)
admin.site.register(Visit, VisitAdmin)

