def transferText(text):
    i = 1
    if text:
        newText = text[0].upper()
    while(i < len(text)):
        if (text[i].isspace()):
            newText += text[i:i+2].upper()
            i +=1
        else:
            newText += text[i].lower()
        i += 1
    return newText if newText else text 
    

class Guest:
    __slots__ = ("__username","__password","__fullname","__email","__address","__role")
    def __init__(self,username,password,fullname,email,address,role):
        self.__username = username
        self.__password = password
        self.__fullname = transferText(fullname)
        self.__email = email
        self.__address = address
        self.__role = role
    @property
    def role(self):
        return self.__role
    @property
    def userName(self):
        return self.__username
    def setUser(self,newUser):
        self.__username = newUser
        return True
    @property
    def Pass(self):
        return self.__password
    def setPass(self,newPass):
        if len(newPass) < 6 or len(newPass) > 100:
            return False
        self.__password = newPass
        return True
    @property
    def email(self):
        return self.__email
    def setEmail(self,newEmail):
        self.__email = newEmail 
        return True
    @property
    def address(self):
        return self.__address
    def setAddress(self,address):
        self.__address = address
        return True
    @property
    def name(self):
        return self.__fullname
    def setName(self,newName):
        self.__fullname = transferText(newName)
        return True