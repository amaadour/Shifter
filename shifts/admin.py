from django.contrib import admin
from .models import User,Staff,Arrangement,Day

# Register your models here.
@admin.action(description='Clear Arrangements')
def resetArrangement(modelAdmin,request, queryset:Arrangement):
    for query in queryset:
        query.staffSet.all().delete()
        Day.objects.filter(arrangement = query).delete()
        

class StaffAdmin(admin.ModelAdmin):
    readonly_fields=["daysWorked"]

class ArrangementAdmin(admin.ModelAdmin):
    actions=[resetArrangement]

admin.site.register(User)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Arrangement,ArrangementAdmin)
admin.site.register(Day)