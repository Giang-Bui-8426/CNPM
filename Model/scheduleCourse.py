from datetime import datetime
class ScheduleCourse:
    __slots__ = ("__scheduleID","__dateStart","__dateEnd","__session","__dayOfWeek")
    def __init__(self,scheduleID,start,end,session,day):
        self.__scheduleID = scheduleID
        self.__dateStart = start 
        self.__dateEnd = end
        self.__session = session
        self.__dayOfWeek = day
    @property
    def scheduleID(self):
        return self.__scheduleID
    @property
    def session(self):
        return self.__session
    @property
    def dayOfWeek(self):
        return self.__dayOfWeek
    @property
    def dateStart(self):
        return self.__dateStart
    @property
    def dateEnd(self):
        return self.__dateEnd
    def __eq__(self, scheduleOther):
        check1 = max(datetime.strptime(self.__dateStart,"%d/%m/%Y"),datetime.strptime(scheduleOther.dateStart,"%d/%m/%Y")) 
        check2 =  min(datetime.strptime(scheduleOther.dateEnd,"%d/%m/%Y"),datetime.strptime(self.__dateEnd,"%d/%m/%Y"))
        day = self.__dayOfWeek == scheduleOther.dayOfWeek
        session = int(self.__session) == int(scheduleOther.session)
        return (check1 <= check2 and day and session)