from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.urls import reverse_lazy
from .util import daysInPeriod
# Create your models here.
class User(AbstractUser):
    pass

class Staff(models.Model):

    name=models.CharField(max_length=50,null=True)
    daysWorked = models.IntegerField(default= 0)
    username = models.CharField(max_length= 50,null= False,blank= False)
    
    def save(self):
        if self.name == None:
            self.name=self.username
        super(Staff,self).save()
    def getDaysWorked(self):
        return self.daysWorked

    def checkin(self):
        self.daysWorked+=1
        self.save()
        return self.daysWorked

    def __str__(self):
        return self.username
    
    

class Arrangement(models.Model):

    staffSet= models.ManyToManyField(Staff,related_name="AvailabeStaff") 
    title = models.CharField(max_length=50,null=False)
    start=models.DateField(("Starting date"), auto_now=False, auto_now_add=False)
    end=models.DateField(("Finish date"), auto_now=False, auto_now_add=False)
    minDaysOff=models.IntegerField("Off days",default=1)
    is_filled = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('fill', kwargs={'pk': self.pk})

    def reset(self):
        queryset = Day.objects.filter(arrangement= self)
        for staff in self.staffSet.all():
            staff.daysWorked=0
        for day in queryset:
            day.staffSet.clear()
            day.save()
        
    def resetDays(self) -> None:
        calendar = daysInPeriod(self.start,self.end)
        try:    
            reset = Day.objects.filter(arrangement = self)
            for day in reset:
                day.delete(keep_parents=True)
            print("reset arrangement")
        except:
            pass
        for day in calendar:
            Day.objects.create(date=day,arrangement = self)

    def is_possible(self)->bool:
        staffCount = self.staffSet.all().count()
        dayCount = Day.objects.filter(arrangement=self).count()
        possibleShifts = staffCount*(dayCount-self.minDaysOff)
        requiredShifts = 0
        for day in Day.objects.filter(arrangement=self):
            requiredShifts+=day.minStaff
            if day.minStaff>staffCount:
                return False
        if requiredShifts>possibleShifts:
            return False
        else: return True

        
        
    def arrange(self):
        self.reset()
        staffList = list(self.staffSet.all())
        dayList = Day.objects.filter(arrangement=self)
        requiredDays = len(dayList)-self.minDaysOff
        if self.is_possible():
            for day in dayList:
                for i in range(day.getMinStaff()):
                    try:
                        day.staffSet.add(staffList[0])
                        if staffList[0].checkin()<requiredDays:
                            staffList.append(staffList.pop(0))
                        else: 
                            staffList.pop(0)
                    except IndexError:
                        pass
                    
            
            i,j=0,0
            while len(staffList)>0:
                while staffList[0] in dayList[i].staffSet.all() and j<len(staffList):
                    staffList.append(staffList.pop(0))
                    j+=1
                j=0

                dayList[i].staffSet.add(staffList[0])
                if staffList[0].checkin() <requiredDays:
                    staffList.append(staffList.pop(0))
                else: 
                    staffList.pop(0)
                i+=1
            
        else:
            while len(staffList)>0:
                for day in dayList:
                    if day.staffSet.all().count()<day.minStaff and not day.staffSet.all().count()==len(staffList):
                        for staff in staffList:
                            if staff not in day.staffSet.all():
                                day.staffSet.add(staff)
                                if staff.checkin()>=requiredDays:
                                    staffList.remove(staff)
                                break
        for day in dayList:
            day.save()


class Day(models.Model):

    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"


    date    = models.DateField(auto_now= False, auto_now_add= False,null=False)
    staffSet= models.ManyToManyField(Staff,related_name="DayStaff")
    minStaff=models.IntegerField(default= 1)
    arrangement = models.ForeignKey(Arrangement, on_delete=models.CASCADE,related_name="parent_arrangement",default=1)

    def __str__(self):
        return (f"{self.date.month}/{self.date.day}/{self.date.year} - {self.arrangement}")

    def setMinStaff(self,num):
        if isinstance(num,int):
            self.minStaff = num
            return num
        else: raise TypeError("Type error value is not an integer")
    
    def getMinStaff(self):
        return self.minStaff
    
    def printStaff(self)->str:
        staff = list(self.staffSet.all())
        staffStr = ""
        for staf in staff:
            staffStr+=str(staf)+" "
        return staffStr
    


