#Singleton to keep track of the processes running. For now, only encompasses schedules. Need to keep track if cancellation is needed.
class processMonitor:
  #Current Singleton instance
  currentInstance = None
  #Keep track of # of running schedules
  runningSchedules = 0
  #Intended to alert a particular scheduled process on whether it needs to be cancelled
  alertedSchedule = 0
  #Keep track of some information to display to the discord user
  scheduleInfo = ""

  #Called to get the singleton instance, if any
  def getInstance():
    if(processMonitor.currentInstance == None):
      processMonitor.currentInstance = processMonitor()
    return processMonitor.currentInstance

  #Is called each time a new schedule is generated. This will allow it to keep track of all the schedules available. Makes it easier for us to cancel the task if need be
  def newSchedule(self, info):
    #Increment the # of running schedules
    self.runningSchedules += 1

    #Add the information on this new process to the informational list
    self.scheduleInfo += (str(self.runningSchedules) + info)

    #Return an identifier to that particular scheduled process so it can watch the singleton to see if an alert was sent out
    identifier = self.runningSchedules
    return identifier
  
  #Alert a particular scheduled process
  def alertSchedule(self, scheduleToAlert):
    self.alertedSchedule = scheduleToAlert
  
  #If the process identifier matches the alerted schedule, reset the alertedSchedule variable, and return True. Else returns False
  def checkAlerts(self, processIdentifier):
    if(processIdentifier == self.alertedSchedule):
      self.alertedSchedule = 0
      return True
    else:
      return False
  
  #Display information for the discord user if they want to view the schedules, or cancel a schedule by chance
  def giveInfo(self):
    return self.info

  #Initialize the singleton
  def __init__(self):
    if processMonitor.currentInstance != None:
      raise Exception("Already exists")
    else:
      processMonitor.currentInstance = self
