import re
def transferText(text):
    i = 1
    newText = text[0].upper()
    while(i < len(text)):
        if (text[i].isspace()):
            newText += text[i:i+2].upper()
            i +=1
        else:
            newText += text[i].lower()
        i += 1
    return newText
class Guest:
    __slots__ = ("__username","__password","__fullname","__email","__address","__role")
    def __init__(self,username,password,fullname,email,address,role):
        self.__username = username
        self.__password = password
        self.__fullname = fullname
        self.__email = email
        self.__address = address
        self.__role = role
    @property
    def getRole(self):
        return self.__role
    @property
    def getUserName(self):
        return self.__username
    def setUser(self,newUser):
        if len(newUser) < 6 or len(newUser) > 50 or re.search(r'[^A-Za-z0-9]',newUser):
            return False
        self.__username = newUser
        return True
    @property
    def getPass(self):
        return self.__password
    def setPass(self,newPass):
        if len(newPass) < 6 or len(newPass) > 100:
            return False
        self.__password = newPass
        return True
    @property
    def getEmail(self):
        return self.__email
    def setEmail(self,newEmail):
        if re.findall(r"(\@)",newEmail):
            user = newEmail.split("@")
            if 6 > len(user[0]) or len(user[0]) > 64:
                return False
            if user[1][0] == "." or user[1][-1] == "." or not re.findall(r"(\.)",user[1]):
                return False
            self.email = newEmail 
            return True
        else:
            return False
    @property
    def getAddress(self):
        return self.__address
    def setAddress(self,address):
        self.__address = address
        return True
    @property
    def getName(self):
        return self.__fullname
    def setName(self,newName):
        if re.search(r'[^A-Za-z0-9 ]',newName):
            return False
        self.__fullname = transferText(newName)
        return True