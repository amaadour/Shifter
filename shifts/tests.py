from django.test import TestCase
from typing import List

class Staff:
    def __init__(self,name:str) -> None:
        self.name = name
        self.daysWorked = 0
    def checkout(self):
        self.daysWorked+=1
        return self.daysWorked
    def __str__(self) -> str:
        return self.name
class Day:
    def __init__(self,count,minStaff:int) -> None:
        self.staffArr = []
        self.num=count
        self.minStaff=minStaff

    def addStaff(self,staff:Staff):
        self.staffArr.append(staff)
    def getMinStaff(self):
        return self.minStaff

    def getNum(self):
        return self.num
    
    def getStaff(self):
        return self.staffArr

    def reset(self):
        self.staffArr=[]
    def print(self):
        names=""
        for staff in self.staffArr:
            names+=staff.name+", "
        print(self.num,": ",names)

class Arrangement:
    def __init__(self,title:str,days=[],off=1,) -> None:
        self.staffArr = []
        self.dayArr = []
        for i in range(len(days)):
            self.dayArr.append(Day(i,days[i]))
        self.minDaysOff = off
        self.title=title
        self.done = False

    def getDayCount(self)->int:
        return len(self.staffArr)
    
    def addStaff(self,staff:Staff):
        self.staffArr.append(staff)
        self.done=False

    def is_satisfied(self)->bool:
        availableShifts = len(self.staffArr)*(len(self.dayArr)-self.minDaysOff)
        requiredShifts = 0
        for i in range(len(self.dayArr)):
            requiredShifts+=self.dayArr[i].getMinStaff()
            if self.dayArr[i].getMinStaff() > len(self.staffArr):
                return False
        if requiredShifts>availableShifts:
            return False
        return True
    def reset(self):
        for day in self.dayArr:
            day.reset()
    
    def arrange(self):
        if self.done:
            return self.dayArr
        self.reset()
        staffQ = self.staffArr
        requiredDays = len(self.dayArr)-self.minDaysOff
        if self.is_satisfied():
            for day in self.dayArr:
                for i in range(day.getMinStaff()):
                    try:
                        day.addStaff(staffQ[0])
                        if staffQ[0].checkout()<requiredDays:
                            staffQ.append(staffQ.pop(0))
                        else: staffQ.pop(0)
                    except:
                        pass
                    
            i,j=0,0
            while len(staffQ)>0:
                while staffQ[0] in self.dayArr[i%len(self.dayArr)].getStaff() and j<len(staffQ):
                    staffQ.append(staffQ.pop(0))
                    j+=1
                j=0                    
                
                self.dayArr[i%len(self.dayArr)].addStaff(staffQ[0])
                if staffQ[0].checkout()<requiredDays:
                    staffQ.append(staffQ.pop(0))
                else: staffQ.pop(0)
                i+=1
        else:
            while len(staffQ)>0:
                for day in self.dayArr:
                    if len(day.getStaff())<day.getMinStaff() and not len(day.getStaff())==len(staffQ):
                        for staff in staffQ:
                            if staff not in day.getStaff():
                                day.addStaff(staff)
                                if staff.checkout()>=requiredDays:
                                    staffQ.remove(staff)
                                break
                

    
    def print(self):
        for day in self.dayArr:
            day.print()


dayArr = [2,3,1,2,3,4,2]
shifts = Arrangement("shifts",dayArr,4)
staff = ["Bachir","Bacha","Aymene","Said","Brotha"]

for staf in staff:
    shifts.addStaff(Staff(staf))
shifts.arrange()
shifts.print()




