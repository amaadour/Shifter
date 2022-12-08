import datetime

def daysInPeriod(start,end)->list[datetime.datetime]:
    calendar = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
    return calendar