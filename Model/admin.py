from guest import Guest
class Admin(Guest):
    __slots__ = ("__adminID")
    def __init__(self,adminID,password,fullname,email,address):
        super().__init__(username=adminID, password=password, fullname=fullname, email=email, address=address,role='admin')
        self.__adminID = adminID
    @property
    def getAdminID(self):
        return self.__adminID
    def setAdminID(self,new):
        self.__adminID = new