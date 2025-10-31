import stores

class accountController:
    def __init__(self,stores):
        self.stores = stores
    def login(self,username,password):
        if self.stores.students[username]:
            if self.stores.students[username]["password"] == password:
                return "student"
            else: return ""
        elif self.stores.admin[username]:
            if self.stores.students[username]["password"] == password:
                return "admin"
            else:
                return ""
        else:
            return ""
    def changePass(self,mssv,newPass,oldPass):
        st = s.stores.student[mssv]
        if st.getPass != oldPass:
            return "oldPass"
        if not st.setPass(newPass):
            return "newPass"
        else: return ""
        
    def updateProfile(self,mssv,name="",email="",major="",address=""):
        if name:
            if not (s.stores.student[mssv].setName(name)):
                return False
        if email:
            if not (s.stores.student[mssv].setEmail1(email)):
                return False
        if major:
            if not (s.stores.student[mssv].setMajor(major)):
                return False
        if address:
            if not (s.stores.student[mssv].setAddress(address)):
                return False
        self.stores.save_students()
        return True
            
        