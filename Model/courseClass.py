class CourseClass:
    __slots__ = ("__classID","__courseID","__roomID","__maxStudents","__status","__scheduleID","__student")
    def __init__(self,classID,courseID,roomID,maxStudents,status,scheduleID,student=None):
        self.__classID = classID
        self.__courseID = courseID
        self.__roomID = roomID
        self.__maxStudents = maxStudents
        self.__status = status
        self.__scheduleID = scheduleID
        self.__student = list(student) if student else []
    @property
    def classID(self):
        return self.__classID
    @property
    def courseID(self):
        return self.__courseID
    @property
    def roomID(self):
        return self.__roomID
    def setRoomID(self,ID):
        self.__roomID = ID 
    @property
    def maxStudents(self):
        return self.__maxStudents
    @property
    def status(self):
        return self.__status
    def setStatus(self,status = "open"):
        self.__status = status
        return True
    @property
    def scheduleID(self):
        return self.__scheduleID
    @property
    def students(self):
        return self.__student
    @property
    def amountStudent(self):
        return len(self.__student)
    def addStudent(self,StudentID,add =True):
        if add:
            if isinstance(StudentID,list):
                self.__student.extend(StudentID)
            else:
                self.__student.append(StudentID)
        else:
            if StudentID in self.__student:
                self.__student.remove(StudentID)
            else: return False
        return True
    def setStudent(self,ListStudent):
        self.__student = ListStudent

    