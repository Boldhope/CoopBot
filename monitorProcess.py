class scheduleContainer:
    scheduledDate = ""
    gameTitle = ""
    memberList = []


#TO DO:
#Add memberList variable to the singleton, so that it can keep track of the members which need to be alerted
#Add method of displaying participants for a particular schedule
#Potentially use a dictionary which identifies the scheduled process + the name of the member(s) (there may be multiple members for a given key)
#Singleton to keep track of the processes running. For now, only encompasses schedules. Need t  o keep track if cancellation is needed.
class processMonitor:
    #Current Singleton instance
    currentInstance = None
    
    #Keep track of # of running schedules
    runningSchedules = 0
    
    #Intended to alert a particular scheduled process on whether it needs to be cancelled
    alertedSchedule = 0

    #Dictionary to keep track of the list of members, the string associated with each scheduled process
    scheduleLookup = {}

    #Called to get the singleton instance, if any
    def getInstance():
        if (processMonitor.currentInstance == None):
            processMonitor.currentInstance = processMonitor()
        return processMonitor.currentInstance

    #Is called each time a new schedule is generated. This will allow it to keep track of all the schedules available. Makes it easier for us to cancel the task if need be
    def newSchedule(self, dayOfWeek, timeOfDay, amOrPM, timeZone):
        #Increment the # of running schedules
        self.runningSchedules += 1

        #Add the information on this new process to the informational list, needs work...
        #self.scheduleInfo += (str(self.runningSchedules) + info)

        #Return an identifier to that particular scheduled process so it can watch the singleton to see if an alert was sent out
        identifier = self.runningSchedules

        print(timeOfDay)
        #Add information to the dictionary
        info = scheduleContainer()
        info.scheduledDate = "set for " + dayOfWeek + " at " + timeOfDay + " " + amOrPM + " " + timeZone
        #info.gameTitle = specifiedGame #needs to check if valid game as well on the game list before validating this. TO DO
        self.scheduleLookup[identifier] = info

        return identifier

    #Alert a particular scheduled process
    def alertSchedule(self, scheduleToAlert):
        #If there is no ongoing alert, schedule cancellation
        if (self.alertedSchedule == 0):
            self.alertedSchedule = scheduleToAlert
            return True
        else:
            return False

    #If the process identifier matches the alerted schedule, reset the alertedSchedule variable, and return True. Else returns False
    def checkAlerts(self, processIdentifier):
        print(str(self.alertedSchedule) + " versus " + str(processIdentifier))
        if (int(processIdentifier) == int(self.alertedSchedule)):
            self.alertedSchedule = 0
            return True
        else:
            return False

    #Display information for the discord user if they want to view the schedules, or cancel a schedule by chance
    def giveInfo(self):
        listOfKeys = self.scheduleLookup.keys()
        strToDisp = ""
        for i in listOfKeys:
          strToDisp = strToDisp + str(i) + ") " + self.scheduleLookup[i].scheduledDate + "\n"
        
        return strToDisp
        

    #Initialize the singleton
    def __init__(self):
        if processMonitor.currentInstance != None:
            raise Exception("Already exists")
        else:
            processMonitor.currentInstance = self
