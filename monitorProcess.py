#--------------------------------------------------------
# monitorProcess.py
# What it does: A singleton class that keeps track of all of the information/processes running for schedules for the bot.
# Dependencies: asyncio, commandSupport.py, dataStructs.py
#--------------------------------------------------------
#Notes: TO DO:
#       Potentially use a dictionary which identifies the scheduled process + the name of          
#       the member(s) (there may be multiple members for a given key)
#       Singleton to keep track of the processes running. For now, only encompasses schedules. Need to keep track if cancellation #       is needed.
#       May want to randomize the key generation, so that we aren't specifically tied down whenever a removal happens. & list this as a schedule ID when listing schedule.
#       Fix the issue with time zones, when the user enters anything other than utc.
#       Add participant names to each schedule when listing schedule

from commandSupport import *
from dataStructs import *
import asyncio

class processMonitor:
    #Current Singleton instance
    currentInstance = None
    
    #Keep track of # of running schedules
    runningSchedules = 0
    
    #Intended to alert a particular scheduled process on whether it needs to be cancelled
    alertedSchedule = 0

    #Dictionary to keep track of the list of members, the string associated with each scheduled process
    scheduleLookup = {}

    #Dictionary to keep track of the tasks.
    taskList = {}
    #Called to get the singleton instance, if any
    def getInstance():
        if (processMonitor.currentInstance == None):
            processMonitor.currentInstance = processMonitor()
        return processMonitor.currentInstance

    #Is called each time a new schedule is generated. This will allow it to keep track of all the schedules available. Makes it easier for us to cancel the task if need be
    def newSchedule(self, dayOfWeek, timeOfDay, amOrPM, timeZone):
        #Increment the # of running schedules
        self.runningSchedules += 1

        identifier = self.runningSchedules
        #Find out what day it is, for reference. Make this a separate function when done. Returns dayinTermsofNum for use later to find the day.
        dayinTermsOfNum = 0
        for day in Days:
          if(day.name == dayOfWeek.lower()):
            dayinTermsOfNum = day.value

        #Separate timeOfDay into hour and minutes
        actualTime = timeOfDay.split(':')
        actualMinutes = int(actualTime[1])
        actualTimeZone = timeZone.lower()
        
        #Figure out the actual hour offset, based on whether we are in PM or AM.
        actualHours = 0
        dayOrNight = amOrPM.lower()
        if(dayOrNight == "am"):
          actualHours = int(actualTime[0])
        else:
          actualHours = int(actualTime[0]) + 12
      
        #Add information to the dictionary
        info = scheduleContainer()
        info.scheduledDate = "set for " + dayOfWeek + " at " + timeOfDay + " " + amOrPM + " " + timeZone

        newTask = asyncio.create_task(monitorTime(actualHours, actualMinutes, dayinTermsOfNum, actualTimeZone, info))

        #Add the new task to the dictionary of tasks and schedule dictionary
        self.taskList[identifier] = newTask
        self.scheduleLookup[identifier] = info

    #Delete a particular task
    def removeSchedule(self, scheduleToAlert):
        loneSchedule = self.taskList.get(int(scheduleToAlert))
        loneSchedule.cancel()
        #Remove all traces of the schedule we wanted to remove >:o
        del self.taskList[int(scheduleToAlert)]
        del self.scheduleLookup[int(scheduleToAlert)]

        self.runningSchedules -= 1
        print("Successfully removed")
        
        return True

    #Allow the user to add a game to the planned date.
    def addGame(self, scheduleIdentifier,gameName):
      scheduleKey = int(scheduleIdentifier)
      if (scheduleKey in self.scheduleLookup.keys()):
        desiredSchedule = self.scheduleLookup.get(int(scheduleIdentifier))

        if(desiredSchedule.gameTitle == ""):
          desiredSchedule.gameTitle = gameName
          return True

        else:
          return False

      return False

    #Append the discord user/member object to the list of users objects for a particular scheduled time.
    def addMember(self, scheduleIdentifier, discordUser):
      scheduleKey = int(scheduleIdentifier)
      if (scheduleKey in self.scheduleLookup.keys()):
        desiredSchedule = self.scheduleLookup.get(scheduleKey)
        desiredSchedule.memberList.append(discordUser)

    #Display information for the discord user if they want to view the schedules, or cancel a schedule by chance
    def giveInfo(self):
        strToDisp = ""
        if(bool(self.scheduleLookup)):
          listOfKeys = self.scheduleLookup.keys()
          for i in listOfKeys:
            strToDisp = strToDisp + self.scheduleLookup[i].gameTitle + " " + self.scheduleLookup[i].scheduledDate + "\n"
        else:
          strToDisp = "No schedules currently active."
        return strToDisp
        

    #Initialize the singleton
    def __init__(self):
        if processMonitor.currentInstance != None:
            raise Exception("Already exists")
        else:
            processMonitor.currentInstance = self
