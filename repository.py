
import os, csv, tempfile
from typing import Dict, List
from Model.courseClass import CourseClass 
from Model.scheduleCourse import ScheduleCourse
from Model.student import Student 
from Model.registration import Registration
from Model.debtRecord import DebtRecord
from Model.admin import Admin
from Model.guest import Guest
from Model.course import Course

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
CSV_STUDENTS  = os.path.join(DATA_DIR, "students.csv")
CSV_COURSES   = os.path.join(DATA_DIR, "courses.csv")
CSV_CLASSES   = os.path.join(DATA_DIR, "classes.csv")
CSV_REGS      = os.path.join(DATA_DIR, "registrations.csv")
CSV_DEBTS     = os.path.join(DATA_DIR, "debts.csv")
CSV_SCHEDULES = os.path.join(DATA_DIR, "schedules.csv")

def _read_csv(path):
    if not os.path.exists(path): return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _write_csv(path, rows, fieldnames):
    os.makedirs(DATA_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=DATA_DIR, prefix=os.path.basename(path), suffix='.tmp'); os.close(fd)
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

    def bootstrap(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        def wfile(p, text):
            if not os.path.exists(p):
                with open(p, 'w', encoding='utf-8', newline='') as f: f.write(text.strip()+'\n')
        # Seed
        wfile(CSV_STUDENTS, """mssv,password,fullname,role,email,address,major,completedCourse,debtID
AD001,admin123,Admin,admin,admin@ut.edu.vn,,admin,
SV003,123456,Bui Truong Giang,student,buitruonggiang@gmail.com,Ho Chi Minh City,Information Technology,C015|C010,D002
SV002,123456,Dao The Bao,student,thebaodao@gmail.com,Ho Chi Minh City,Information Technology,C001,D001
""")
        wfile(CSV_COURSES, """courseID,courseName,credit,prereq
C004,Software Technology,2,C001
C003,Python Programming,3,
C002,Databases,3,
C001,Data Structures,3,C003
""")
        wfile(CSV_SCHEDULES, """scheduleID,dateStart,dateEnd,session,dayOfWeek
S001,20/09/2025,20/12/2025,1,Tuesday
S002,21/09/2025,21/12/2025,2,Wednesday
S003,21/09/2025,21/12/2025,3,Friday
S004,20/09/2025,20/12/2025,1,Monday
        """)
        wfile(CSV_CLASSES, """classID,courseID,roomID,scheduleID,maxStudents,status,students
L012,C002,LabA1,S001,30,open,SV002
L013,C003,LabB2,S002,30,open,
L014,C004,HallC3,S003,40,open,
L015,C004,HallA2,S004,40,open,
        """)
        wfile(CSV_REGS, "registrationID,status,mssv,classID\nR001,active,SV002,L012\n")
        wfile(CSV_DEBTS, "debtID,debt\nD001,0\nD002,12000\nD003,0\n")
        self.load()

    def load(self):
        # students
        self.students.clear()
        for r in _read_csv(CSV_STUDENTS):
            if r["role"] == "student":
                s = Student(r['mssv'], r['password'], r['fullname'], r['email'], r['address'], r['major'],
                            r['debtID'], [p for p in (r['completedCourse'] or '').split('|') if p])
                self.students[r['mssv']] = s
            else:
                a = Admin(r['mssv'], r['password'], r['fullname'],r['email'], r['address'])
                self.admins[r['mssv']] = a
        # courses
        self.courses.clear()
        for r in _read_csv(CSV_COURSES):
            self.courses[r['courseID']] = Course(r['courseID'], r['courseName'], [p for p in (r['prereq'] or '').split('|') if p], int(r['credit']))
        # schedules
        self.schedules.clear()
        for r in _read_csv(CSV_SCHEDULES):
            self.schedules[r['scheduleID']] = ScheduleCourse(r['scheduleID'], r['dateStart'], r['dateEnd'], int(r['session']), r['dayOfWeek'])
        # classes
        self.classes.clear()
        for r in _read_csv(CSV_CLASSES):
            self.classes[r['classID']] = CourseClass(r['classID'], r['courseID'], r['roomID'], int(r['maxStudents']), r['status'],r['scheduleID'])
        # regs
        self.regs.clear()
        for r in _read_csv(CSV_REGS):
            self.regs.append(Registration(r['registrationID'], r['classID'], r['mssv']))
        # debts
        self.debts.clear()
        for r in _read_csv(CSV_DEBTS):
            self.debts[r['debtID']] = DebtRecord(r['debtID'], int(r['debt']))
        # fill students list in each class
        for cl in self.classes.values() :
            cl.addStudent([rg.mssv for rg in self.regs if rg.classID==cl.classID and rg.status == "active"])

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
        _write_csv(CSV_STUDENTS, rows, ['mssv','password','fullname','role','email','address','major','completedCourse','debtID'])

    def save_courses(self):
        rows = [{'courseID':c.courseID,'courseName':c.courseName,'credit':c.credit,'prereq':'|'.join(c.prerequisites)} for c in self.courses.values()]
        _write_csv(CSV_COURSES, rows, ['courseID','courseName','credit','prereq'])

    def save_schedules(self):
        rows = [{'scheduleID':s.scheduleID,'dateStart':s.dateStart,'dateEnd':s.dateEnd,'session':s.session,'dayOfWeek':s.dayOfWeek} for s in self.schedules.values()]
        _write_csv(CSV_SCHEDULES, rows, ['scheduleID','dateStart','dateEnd','session','dayOfWeek'])

    def save_classes(self):
        rows = [{'classID':cl.classID,'courseID':cl.courseID,'roomID':cl.roomID,'scheduleID':cl.scheduleID,'maxStudents':cl.maxStudents,'status':cl.status} for cl in self.classes.values()]
        _write_csv(CSV_CLASSES, rows, ['classID','courseID','roomID','scheduleID','maxStudents','status'])
    def save_regs(self):
        rows = [{'registrationID':r.registrationID,'mssv':r.mssv,'classID':r.classID} for r in self.regs if r.status=='active']
        _write_csv(CSV_REGS, rows, ['registrationID','mssv','classID','status'])

    def save_debts(self):
        rows = [{'debtID':d.debtID,'debt':d.debt} for d in self.debts.values()]
        _write_csv(CSV_DEBTS, rows, ['debtID','debt'])


