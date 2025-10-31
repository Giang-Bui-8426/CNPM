class Student:
    __slots__ = ("__mssv","__completedCourse","__DebtID","__major")
    def __init__(self,mssv,password,fullname,email,address,major,DebtID,completedCourse = []):
        super().__init__(username=mssv, password=password, fullname=fullname, email=email, address=address,role="student")
        self.__mssv = mssv
        self.__completedCourse = completedCourse
        self.__DebtID = DebtID
        self.__major = major
    @property
    def getMssv(self):
        return self.__mssv
    @property
    def getCourse(self):
        return self.__completedCourse
    @property
    def getDebtID(self):
        return self.__DebtID
    @property
    def getMajor(self):
        return self.__major
    def setMajor(self,newMajor):
        self.__major = newMajor
        return True
    def addCompletedCourse(self,courseID,add = True):
        if add:
            self.__completedCourse.append(courseID)
        else:
            if courseID in self.__completedCourse:
                self.__completedCourse.remove(courseID)
            else: False
        return True