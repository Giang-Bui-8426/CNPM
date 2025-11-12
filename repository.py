
import os, csv, tempfile
from Model.courseClass import CourseClass 
from Model.scheduleCourse import ScheduleCourse
from Model.student import Student 
from Model.registration import Registration
from Model.debtRecord import DebtRecord
from Model.admin import Admin
from Model.guest import Guest
from Model.course import Course

dataFolder = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
pathStudents  = os.path.join(dataFolder, "students.csv")
pathCourses   = os.path.join(dataFolder, "courses.csv")
pathClasses   = os.path.join(dataFolder, "classes.csv")
pathRegs      = os.path.join(dataFolder, "registrations.csv")
pathDebts     = os.path.join(dataFolder, "debts.csv")
pathSchedules = os.path.join(dataFolder, "schedules.csv")

def _read_csv(path):
    if not os.path.exists(path): return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _write_csv(path, rows, fieldnames):
    os.makedirs(dataFolder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dataFolder, prefix=os.path.basename(path), suffix='.tmp'); os.close(fd)
    with open(tmp, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)
    os.replace(tmp, path)

class Repository:
    def __init__(self):
        self.students = {}
        self.admins = {}
        self.courses = {}
        self.schedules = {}
        self.classes = {}
        self.regs = []
        self.debts = {}
    def load_accounts(self):
        self.students.clear()
        for r in _read_csv(pathStudents):
            if r["role"] == "student":
                s = Student(r['mssv'], r['password'], r['fullname'], r['email'], r['address'], r['major'],
                            r['debtID'], [p for p in (r['completedCourse'] or '').split('|') if p])
                self.students[r['mssv']] = s
            else:
                a = Admin(r['mssv'], r['password'], r['fullname'],r['email'], r['address'])
                self.admins[r['mssv']] = a
    def load_courses(self):
        self.courses.clear()
        for r in _read_csv(pathCourses):
            self.courses[r['courseID']] = Course(r['courseID'], r['courseName'], [p for p in (r['prereq'] or '').split('|') if p], int(r['credit']))
    # schedules
    def load_schedules(self):
        self.schedules.clear()
        for r in _read_csv(pathSchedules):
            self.schedules[r['scheduleID']] = ScheduleCourse(r['scheduleID'], r['dateStart'], r['dateEnd'], int(r['session']), r['dayOfWeek'])
    def load_classes(self):
        # classes
        self.classes.clear()
        for r in _read_csv(pathClasses):
            self.classes[r['classID']] = CourseClass(r['classID'], r['courseID'], r['roomID'], int(r['maxStudents']), r['status'],r['scheduleID'])
    def load_regs(self):
        self.regs.clear()
        for r in _read_csv(pathRegs):
            self.regs.append(Registration(r['registrationID'], r['classID'], r['mssv']))
        for cl in self.classes.values() :
            cl.addStudent([rg.mssv for rg in self.regs if rg.classID==cl.classID and rg.status == "active"])
    def load_debts(self):
        self.debts.clear()
        for r in _read_csv(pathDebts):
            self.debts[r['debtID']] = DebtRecord(r['debtID'], int(r['debt']))
    def load(self):
        os.makedirs(dataFolder, exist_ok=True)
        def initCsv(path,text):
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8', newline='') as f: 
                    f.write(text.strip()+'\n')
        initCsv(pathStudents,"""mssv,password,fullname,role,email,address,major,completedCourse,debtID
admin123,123456,Admin,admin,admin@ut.edu.vn,,admin, """)
        initCsv(pathClasses,"classID,courseID,roomID,scheduleID,maxStudents,status")
        initCsv(pathCourses, "courseID,courseName,credit,prereq")
        initCsv(pathSchedules, "scheduleID,dateStart,dateEnd,session,dayOfWeek")
        initCsv(pathRegs, "registrationID,mssv,classID")
        initCsv(pathDebts, "debtID,debt")
        # Seed
        self.load_accounts()
        self.load_courses()
        self.load_schedules()
        self.load_debts()
        self.load_classes()
        self.load_regs()
    # Saves
    def save_students(self):
        rows = [{
            'mssv':s.mssv,'password':s.Pass,'fullname':s.name,'role':s.role,
            'email':s.email,'address':s.address,'major':s.major,
            'completedCourse':'|'.join(s.completedCourse),'debtID':s.debtID
        } for s in self.students.values()]
        rows.extend([{
            'mssv':s.adminID,'password':s.Pass,'fullname':s.name,'role':s.role,
            'email':s.email,'address':s.address} for s in self.admins.values()])
        _write_csv(pathStudents, rows, ['mssv','password','fullname','role','email','address','major','completedCourse','debtID'])

    def save_courses(self):
        rows = [{'courseID':c.courseID,'courseName':c.courseName,'credit':c.credit,'prereq':'|'.join(c.prerequisites)} for c in self.courses.values()]
        _write_csv(pathCourses, rows, ['courseID','courseName','credit','prereq'])

    def save_schedules(self):
        rows = [{'scheduleID':s.scheduleID,'dateStart':s.dateStart,'dateEnd':s.dateEnd,'session':s.session,'dayOfWeek':s.dayOfWeek} for s in self.schedules.values()]
        _write_csv(pathSchedules, rows, ['scheduleID','dateStart','dateEnd','session','dayOfWeek'])

    def save_classes(self):
        rows = [{'classID':cl.classID,'courseID':cl.courseID,'roomID':cl.roomID,'scheduleID':cl.scheduleID,'maxStudents':cl.maxStudents,'status':cl.status} for cl in self.classes.values()]
        _write_csv(pathClasses, rows, ['classID','courseID','roomID','scheduleID','maxStudents','status'])
    def save_regs(self):
        rows = [{'registrationID':r.registrationID,'mssv':r.mssv,'classID':r.classID} for r in self.regs if r.status=='active']
        _write_csv(pathRegs, rows, ['registrationID','mssv','classID','status'])

    def save_debts(self):
        rows = [{'debtID':d.debtID,'debt':d.debt} for d in self.debts.values()]
        _write_csv(pathDebts, rows, ['debtID','debt'])


