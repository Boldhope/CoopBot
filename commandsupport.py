import asyncio
import datetime
import pytz

#Will occasionally sleep and let other processes take over, while it tries to wait for the designated time. May have problems that should be looked at later.
async def monitorTime(actualHours, actualMinutes,dayinTermsOfNum, timeZone):
  #Grab initial values of the time.
  t1 = datetime.datetime.now(pytz.timezone(timeZone))

  todayDay = t1.weekday()
  currentHour = t1.hour
  currentMinute = t1.minute

  print("Day :" + str(todayDay) + ", Hour: " + str(currentHour) + ", Min: " + str(currentMinute))

  #loop continuously until we reach the hour and minutes we are looking for.
  while((todayDay != dayinTermsOfNum) and (currentHour != actualHours) and (currentMinute != actualMinutes)):
    #Sleep for one second, before checking the current time again.
    await asyncio.sleep(60)

    #Grab current time...
    t1 = datetime.datetime.now(pytz.timezone(timeZone))

    todayDay = t1.weekday()
    currentHour = t1.hour
    currentMinute = t1.minute

    print("Day Today: " + str(todayDay) + ", Hours: " + str(currentHour) + ", Minutes:" + str(currentMinute))
    