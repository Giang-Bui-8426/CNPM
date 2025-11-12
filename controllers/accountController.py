from Model.student import Student
from Model.debtRecord import DebtRecord
import re

# return id
def autoID(symbol,size,bonus=0):
    id = ""
    size = size+bonus
    if size > 100:
        id = f"{symbol}" + str(size)
    elif size > 10:
        id = f"{symbol}0" + str(size)
    else:
        id = f"{symbol}00" + str(size)
    return id

# return boolean if exactly
def checkEmail(text):
    if re.findall(r"(\@)",text):
        user = text.split("@")
        if len(user) == 2:
            if 6 > len(user[0]) or len(user[0]) > 64:
                return False
            if user[1][0] == "." or user[1][-1] == "." or not re.findall(r"(\.)",user[1]):
                return False
            return True
    else:
        return False

class AccountController:
    def __init__(self,repo):
        self.repo = repo
        
    # return role
    def login(self,username,password):
        if username in self.repo.students:
            if self.repo.students[username].Pass == password:
                return "student"
        elif username in self.repo.admins:
            if self.repo.admins[username].Pass == password:
                return "admin"
        return ""
    
    # return boolean,errors
    def changePass(self,mssv,newPass,oldPass):
        st = self.repo.students[mssv]
        if st.Pass != oldPass:
            return False,"Current password is incorrect"
        if not st.setPass(newPass):
            return False,"Password length must be greater than or equal to 6 and less than 100"
        self.repo.save_students() 
        return True,"ok"
    
    # return về tổng tín chỉ các môn đã đăng ký trong kỳ 
    def current_credits(self, mssv):
        total=0
        for reg in self.repo.regs:
            if reg.mssv==mssv and reg.status=='active':
                total += self.repo.courses[self.repo.classes[reg.classID].courseID].credit
        return total
    
    def user(self,mssv):
        return self.repo.students[mssv]
    
    # return boolean,error
    def updateProfile(self,mssv,name="",email="",major="",address=""):
        if email and not checkEmail(email):
            return False,"Invalid email"
        if name and re.search(r'[^\w\s]',name):
            return False,"Invalid name"
        if major and re.search(r'[^\w\s]',major):
            return False,"Invalid major"
        if address and re.search(r'[^\w\s]',address):
            return False,"Invalid address"
        self.repo.students[mssv].setName(name if name else self.repo.sutdents[mssv].name)
        self.repo.students[mssv].setEmail(email if email else self.repo.sutdents[mssv].email)
        self.repo.students[mssv].setMajor(major if major else self.repo.sutdents[mssv].major)
        self.repo.students[mssv].setAddress(address if address else self.repo.sutdents[mssv].address)
        self.repo.save_students()
        return True,"Ok"
    
    # Return về boolean,errors
    def createAccount(self,mssv,Pass,name,email,addr,major,completed):
        if mssv in self.repo.students:
            return False,"StudentID already exists"
        if mssv[:2] != "SV" or len(mssv[2:]) < 4 or not mssv[2:].isdigit():
            return False,"Pleasant enter correct format of StudentID"
        if email and not checkEmail(email):
            return False,"Please enter correct email format"
        if mssv and (len(mssv) < 6 or len(mssv) > 50) or re.search(r'[^A-Za-z0-9]',mssv):
            return False,"StudentID no validation"
        if Pass and (len(Pass) < 6 or len(Pass) > 50):
            return False,"Password no validation"
        if name and re.search(r'[^\w\s]',name):
            return False,"Name no validation"
        if major and re.search(r'[^\w\s]',major):
            return False,"major no validation"
        debtID = autoID("D",len(self.repo.debts))
        i = 0
        while (debtID in self.repo.debts):
            i += 1
            debtID = autoID("D",len(self.repo.debts),i)
        self.repo.debts[debtID] = DebtRecord(debtID,0)
        self.repo.students[mssv] = Student(mssv,Pass,name,email,addr,major,debtID,completed)
        self.repo.save_debts()
        self.repo.save_students()
        return True,"OK"
        
        
        
            
        