class CourseClass:
    __slots__ = ("__classID","__courseID","__roomID","__maxStudent","__status","__schedule")
    def __init__(self,classID,courseID,roomID,maxStudent,status,schedule):
        self.__classID = classID
        self.__courseID = courseID
        self.__roomID = roomID
        self.__maxStudent = maxStudent
        self.__status = status
        self.__schedule = schedule
        self.__student = []
    @property
    def getClassID(self):
        return self.__classID
    @property
    def getCourseID(self):
        return self.__courseID
    @property
    def getRoomID(self):
        return self.__roomID
    def setRoomID(self,ID):
        self.__roomID = ID 
    @property
    def getMaxStudent(self):
        return self.__maxStudent
    @property
    def getStatus(self):
        return self.__status
    def setStatus(self,status = True):
        self.__status = status
        return True
    @property
    def getSchedule(self):
        return self.__schedule
    @property
    def getStudent(self):
        return self.__student
    @property
    def getAmountStudent(self):
        return len(self.__Student)
    def addStudent(self,StudentID,add =True):
        if add:
            self.__student.append(StudentID)
        else:
            if StudentID in self.__student:
                self.__student.remove(StudentID)
            else: return False
        return True
    def setStudent(self,ListStudent):
        self.__student = ListStudent
    