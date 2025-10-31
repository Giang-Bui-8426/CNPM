class Registration:
    __slots__ = ("__registrationID","__registrationStatus","__classID","__mssv")
    def __init__(self,ID,classID,mssv,Status = "active"):
        self.__registrationID = ID
        self.__registrationStatus = Status
        self.__classID = classID
        self.__mssv = mssv
    @property
    def getRegistrationID(self):
        return self.__registrationID
    @property
    def getRegistrationStatus(self):
        return self.__registrationStatus
    @property
    def getClassID(self):
        return self.__classID
    @property
    def getMssv(self):
        return self.__mssv
    def setRegistrationStatus(self,looked = True):
        self.__registrationStatus = looked
        return looked
    
        