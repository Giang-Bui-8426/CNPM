class ScheduleCourse:
    __slot__ = ("__schedule","__dateStart","__dateEnd","__session","__dayStudy")
    def __init__(self,schedule,start,end,session,day):
        self.__schedule = schedule
        self.__dateStart = start 
        self.__dateEnd = end
        self.__session = session
        self.__dayStudy = day
    @property
    def getSchedule(self):
        return self.__schedule
    @property
    def getSession(self):
        return self.__session
    @property
    def getDayStudy(self):
        return self.__dayStudy
    @property
    def getDateStart(self):
        return self.__dateStart
    @property
    def getDateEnd(self):
        return self.__dateEnd
    def __eq__(self, scheduleOther):
        date = self.__dateEnd <= scheduleOther.getDateStart
        day = self.__dayStudy == scheduleOther.getDayStudy
        session = self.__session == scheduleOther.getSession
        
        return (date and day and session)