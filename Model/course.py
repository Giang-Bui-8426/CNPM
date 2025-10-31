class Course:
    __slots__ = ("__courseID","__courseName","__prerequisites","__credit")
    def __init__(self,courseID,courseName,prerequisites,credit):
        self.__courseID = courseID
        self.__courseName = courseName
        self.__prerequisites = prerequisites
        self.__credit = credit
    @property
    def getCourseID(self):
        return self.__courseID
    @property
    def getCourseName(self):
        return self.__courseName
    @property
    def getPrerequisites(self):
        return self.__prerequisites
    @property
    def getCredit(self):
        return self.__credit
    def setCredit(self,credit):
        if not (isinstance(credit,int)):
            return False
        self.__credit = credit
        return True
    def setPrerequisites(self,ID):
        self.prerequisites = ID
        return True