from django import forms
from .models import *
import datetime
from django.core.exceptions import ValidationError
from .util import daysInPeriod

class ArrangementForm(forms.ModelForm):
    
    class Meta:
        model = Arrangement
        fields = ("title","start","end","minDaysOff")
   
   
    def clean(self):
        clean_data =super().clean()
        start = clean_data.get("start")
        end = clean_data.get("end")
        calendar = daysInPeriod(start,end)
        if len(calendar)>365:
            raise ValidationError("Duration cannot be more than a year")
        if start>end:
            raise ValidationError("End date must be later than start Date",code="date")
        return clean_data

class StaffForm(forms.ModelForm):
    
    class Meta:
        model = Staff
        fields = ["username",]
class DayForm(forms.ModelForm):
    
    class Meta:
        model = Day
        fields = ["minStaff",]
class addForm(forms.Form):
    num = forms.DecimalField()





