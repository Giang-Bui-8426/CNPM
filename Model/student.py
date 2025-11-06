from Model.guest import Guest
class Student(Guest):
    __slots__ = ("__mssv","__completedCourse","__DebtID","__major")
    def __init__(self,mssv,password,fullname,email,address,major,DebtID,completedCourse = None):
        super().__init__(username=mssv, password=password, fullname=fullname, email=email, address=address,role="student")
        self.__mssv = mssv
        self.__completedCourse = (completedCourse or [])
        self.__DebtID = DebtID
        self.__major = major
    @property
    def mssv(self):
        return self.__mssv
    @property
    def course(self):
        return self.__completedCourse
    @property
    def debtID(self):
        return self.__DebtID
    @property
    def major(self):
        return self.__major
    def setMajor(self,newMajor):
        self.__major = newMajor
        return True
    @property
    def completedCourse(self):
        return self.__completedCourse
    def addCompletedCourse(self,courseID,add = True):
        if add:
            self.__completedCourse.append(courseID)
        else:
            if courseID in self.__completedCourse:
                self.__completedCourse.remove(courseID)
            else: return False
        return True