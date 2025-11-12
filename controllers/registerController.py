from Model.registration import Registration
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
class RegisterController:
    def __init__(self,repo):
        self.repo = repo
        self.regs = self.repo.regs
    
    #return sl sinh vien trong lớp
    def amountStudentInClass(self, class_id): 
        return sum(1 for reg in self.regs if reg.classID==class_id and reg.status=='active')
    
    #return boolean
    def conflict_schedule(self,mssv,schedule):
        for reg in self.regs:
            if mssv == reg.mssv and reg.status == "active":
                oldSchedule = self.repo.schedules[self.repo.classes[reg.classID].scheduleID]
                if schedule == oldSchedule:
                    return False,f"Duplicates schedule with classID {reg.classID}"
        return True,"OK"
    
    #return boolean
    def checkMaxCredit(self,mssv,credit,maxCredit =28):
        totalCredit = 0
        for reg in self.regs:
            if mssv == reg.mssv:
                totalCredit += int(self.repo.courses[self.repo.classes[reg.classID].courseID].credit)
        return (totalCredit + credit) <= maxCredit
    
    # return value debts
    def recalc_debt(self, mssv, perCredit = 980000):
        total = 0
        for reg in self.regs:
            if reg.mssv==mssv and reg.status=='active':
                total += self.repo.courses[self.repo.classes[reg.classID].courseID].credit
        debt_value = total * perCredit
        self.repo.debts[self.repo.students[mssv].debtID].setDebt(debt_value) 
        self.repo.save_debts()
        return debt_value
    
    #return boolean,errors
    def register(self,mssv,classID,admin=False):
        if mssv not in self.repo.students:
            return False,"Student no exist"
        if classID not in self.repo.classes:
            return False,"Class no exist"
        if not admin:
            if self.repo.classes[classID].status != "open":
                return False, "Class is locked"
        self.repo.courses[self.repo.classes[classID].courseID]
        for reg in self.regs:
            if reg.mssv == mssv:
                if self.repo.classes[reg.classID].courseID == self.repo.classes[classID].courseID:
                    return False,"Student has attend this course"
            
        check1,tmp1 = self.conflict_schedule(mssv,self.repo.schedules[self.repo.classes[classID].scheduleID])
        if not check1:
            return False,tmp1
        credit = self.repo.courses[self.repo.classes[classID].courseID].credit
        if not self.checkMaxCredit(mssv,credit):
            return False,"Exceeding the maximum number of credits"
        
        if self.amountStudentInClass(classID) >= self.repo.classes[classID].maxStudents:
            return False,"Exceeding the maximum number of students"
        
        id = autoID("R",len(self.regs))
        i = 0
        while (id in self.repo.debts):
            i +=1
            id = autoID("R",len(self.repo.regs),i)
            
        self.repo.classes[classID].addStudent(mssv)
        self.regs.append(Registration(id,classID,mssv))
        self.recalc_debt(mssv)
        self.repo.save_regs()
        self.repo.save_classes()
        return True,"OK"
    
    #return boolean,errors
    def cancelRegister(self,mssv,classID,admin=False):
        for reg in self.regs:
            if reg.mssv == mssv and reg.classID == classID:
                if not admin:
                    if reg.status != "active":
                        return False,"Registered outdate"
                self.repo.classes[classID].addStudent(mssv,add=False)
                self.regs.remove(reg)
                self.recalc_debt(mssv)
                self.repo.save_regs()
                self.repo.save_classes()
                return True,"OK"
        return False,"Cancel registration without success"
        
        
        
            
                    
    