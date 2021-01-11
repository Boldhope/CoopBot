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

  print("Specified Day :" + str(dayinTermsOfNum) + ", Specified Hour: " + str(actualHours) + ", Specified Min: " + str(actualMinutes))
  #loop continuously until we reach the hour and minutes we are looking for.
  while((todayDay != dayinTermsOfNum) or (currentHour != actualHours) or (currentMinute != actualMinutes)):
    #Sleep for one second, before checking the current time again.
    await asyncio.sleep(30)

    #Grab current time...
    t1 = datetime.datetime.now(pytz.timezone(timeZone))

    todayDay = t1.weekday()
    currentHour = t1.hour
    currentMinute = t1.minute

    print("Day Today: " + str(todayDay) + ", Hours: " + str(currentHour) + ", Minutes:" + str(currentMinute))
  
  print("Time reached...")
  #Note TO DO that a specific scheduled time has to be tied to another action, which will alert the users when the task is finished.


  #Obtain user input on the game name in a single string.
def getUserInputtedGameName(args):
  buffer = ""
  #Piece together the arguments into one cohesive string
  for arg in args:
    buffer += (arg + " ")

  #Open the file and check if it is already in the list
  buffer = buffer.rstrip()
    
  return buffer
