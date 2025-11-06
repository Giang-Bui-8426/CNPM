class Registration:
    __slots__ = ("__registrationID","__registrationStatus","__classID","__mssv")
    def __init__(self,ID,classID,mssv,status = "active"):
        self.__registrationID = ID
        self.__registrationStatus = status
        self.__classID = classID
        self.__mssv = mssv
    @property
    def registrationID(self):
        return self.__registrationID
    @property
    def status(self):
        return self.__registrationStatus
    @property
    def classID(self):
        return self.__classID
    @property
    def mssv(self):
        return self.__mssv
    def setRegistrationStatus(self,looked = "active"):
        self.__registrationStatus = looked
        return looked
    
        