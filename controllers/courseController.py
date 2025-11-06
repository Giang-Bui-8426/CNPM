from datetime import datetime
from Model.course import Course
from Model.scheduleCourse import ScheduleCourse
from Model.courseClass import CourseClass

def autoID(symbol,size):
    id = ""
    if size > 100:
        id = f"{symbol}" + str(size)
    elif size > 10:
        id = f"{symbol}0" + str(size)
    else:
        id = f"{symbol}00" + str(size)
    return id
class CourseController:
    def __init__(self,repo):
        self.repo = repo
        self.courses = self.repo.courses
        self.courseClasses = self.repo.classes
        
    # return False,Erorr nếu nó lỗi , True,Ok nếu không lỗi    
    def addCourse(self,courseID,courseName,prerequisites,credit):
        try:
            if courseID in self.courses:
                return False,"Course already exist"
            credit = int(credit)
            self.courses[courseID] = Course(courseID,courseName,prerequisites,credit)
            self.repo.save_courses()
            return True,"Ok"
        except ValueError as e:
            return False,str(e)
    
    # return False nếu lỗi        
    def removeCourse(self,courseID):
        if courseID in self.courses:
            del self.courses[courseID]
            self.repo.save_courses()
            return True
        return False
    
    # return False,Erorr nếu nó lỗi , True,schedule nếu không lỗi
    def addSchedule(self,start,end,session,day):
        dayOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        try:
            check1 = datetime.strptime(start,"%d/%m/%Y")
            check2 = datetime.strptime(end,"%d/%m/%Y")
            if (check1 > check2): return False, "Invalid start and end dates"
            day = day.strip().title()
            if day not in dayOfWeek:
               return False,"Day no validation" 
            session = int(session)
            if 0 > session or session > 5:
                return False,"Session no validation"
            scheduleID = autoID("S",len(self.repo.schedules))
        except ValueError as e:
            return False,str(e)
        else: 
            return True,ScheduleCourse(scheduleID,start,end,session,day)
        
        
    # return False,Erorr nếu nó lỗi , True,class nếu không lỗi
    def addCourseClass(self,classID,courseID,roomID,maxStudents,sched,status="open"):
        try:
            if classID in self.courseClasses:
                return False,"classID already exists."
            for cl in self.repo.classes.values():
                if cl.roomID == roomID:
                    if self.repo.schedules[cl.scheduleID] == sched:
                        return False,"Duplication RoomID"
            maxStudents = int(maxStudents)
            self.repo.classes[classID] = CourseClass(classID,courseID,roomID,maxStudents,status,sched.scheduleID)
            self.repo.schedules[sched.scheduleID] = sched
            self.repo.save_schedules()
            self.repo.save_classes()
            return True,"OK"
        except ValueError as e:
            return False,str(e)
        
    # Xóa lớp
    def removeCourseClass(self,classID):
        try:
            if classID in self.courseClasses:
                del self.courseClasses[classID]
                for r in self.repo.regs:
                    if r.classID == classID:
                        r.setRegistrationStatus("inactive")
            self.repo.save_regs()
            self.repo.save_classes()
            return True,"OK"
        except ValueError as e:
            return False,str(e)
    
    # nút set status
    def lookedStatus(self,classID):
        cl = self.courseClasses[classID]
        cl.setStatus('locked' if cl.status=='open' else 'open')
        self.repo.save_classes()
    
    # xóa sinh viên ra khỏi lớp 
    def removeStudentOutClass(self,mssv,classID):
        if not self.courseClasses[classID].addStudent(mssv,False):
            return False,"Student no exist in class"
        for reg in self.repo.regs:
            if reg.mssv == mssv and reg.classID == classID:
                reg.setRegistrationStatus("inactive")
                break
        return True,"OK"
                
                
        
            
            
        