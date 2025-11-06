class Course:
    __slots__ = ("__courseID","__courseName","__prerequisites","__credit")
    def __init__(self,courseID,courseName,prerequisites,credit):
        self.__courseID = courseID
        self.__courseName = courseName
        self.__prerequisites = prerequisites
        self.__credit = credit
    @property
    def courseID(self):
        return self.__courseID
    @property
    def courseName(self):
        return self.__courseName
    @property
    def prerequisites(self):
        return self.__prerequisites
    @property
    def credit(self):
        return self.__credit
    def setCredit(self,credit):
        if not (isinstance(credit,int)):
            return False
        self.__credit = credit
        return True
    def addPrerequisites(self,ID):
        self.__prerequisites.append(ID)
        return True