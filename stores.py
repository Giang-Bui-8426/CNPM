
import os, csv, tempfile
from typing import Dict, List
from Model import Course, CourseClass, ScheduleCourse, Student, Registration, DebtRecord, Admin, Guest

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "data")
CSV_STUDENTS = os.path.join(DATA_DIR, "students.csv")
CSV_COURSES  = os.path.join(DATA_DIR, "courses.csv")
CSV_CLASSES  = os.path.join(DATA_DIR, "classes.csv")
CSV_REGS     = os.path.join(DATA_DIR, "registrations.csv")
CSV_DEBTS    = os.path.join(DATA_DIR, "debts.csv")
CSV_SCHEDULES= os.path.join(DATA_DIR, "schedules.csv")

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
        self.students: Dict[str, Student] = {}
        self.admin: Admin | None = None
        self.guest: Guest | None = None
        self.courses: Dict[str, Course] = {}
        self.schedules: Dict[str, ScheduleCourse] = {}
        self.classes: Dict[str, CourseClass] = {}
        self.regs: List[Registration] = []
        self.debts: Dict[str, DebtRecord] = {}

    def bootstrap(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        def wfile(p, text):
            if not os.path.exists(p):
                with open(p, 'w', encoding='utf-8', newline='') as f: f.write(text.strip()+'\n')
        # Seed
        wfile(CSV_STUDENTS, """username,password,fullname,role,email,address,major,compeletedCourse,DebtID
AD001,admin123,Admin,admin,admin@ut.edu.vn,,admin,
SV003,123456,Bui Truong Giang,student,buitruonggiang@gmail.com,Ho Chi Minh City,Information Technology,C015|C010,D002
SV002,123456,Dao The Bao,student,thebaodao@gmail.com,Ho Chi Minh City,Information Technology,,D001
""")
        wfile(CSV_COURSES, """courseID,courseName,credit,prereq
C004,Software Technology,2,
C003,Python Programming,3,
C002,Databases,3,C001
C004,Data Structures,3,C001
""")
        wfile(CSV_SCHEDULES, """scheduleID,dateStart,dateEnd,session,dayOfWeek
S001,20/09/2025,20/12/2025,1,Tuesday
S002,21/09/2025,21/12/2025,2,Wednesday
S003,21/09/2025,21/12/2025,3,Friday
S004,20/09/2025,20/12/2025,1,Monday
""")
        wfile(CSV_CLASSES, """classID,courseID,roomID,scheduleID,maxStudent,status,student
C0123,CT02,LabA1,S_C0123,30,open,SV002
C0125,CT03,LabB2,S_C0125,30,open,
C0124,CT01,HallC3,S_C0124,40,open,
C0126,CT00,HallA2,S_C0126,40,open,
""")
        wfile(CSV_REGS, "registrationID,Status,mssv,classID,\nR001,open,SV002,C0123\n")
        wfile(CSV_DEBTS, "DebtID,Debt\nD001,0\nD002,12000\nD003,0\n")
        self.load()

    def load(self):
        # students
        self.students.clear()
        for r in _read_csv(CSV_STUDENTS):
            if r["role"] == "student":
                s = Student(r['username'], r['password'], r['fullname'], r['email'], r['address'], r['major'],
                            r['debtID'], [p for p in (r['completedCourse'] or '').split('|') if p])
                self.students[r['username']] = s
            else:
                a = Admin(r['username'], r['password'], r['fullname'],r['email'], r['address'])
                self.admin[r['username']] = a
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
            sched = self.schedules[r['scheduleID']]
            self.classes[r['classID']] = CourseClass(r['classID'], self.courses[r['courseID']], r['roomID'], int(r['maxStudent']), r['status'],sched)
        # regs
        self.regs.clear()
        for r in _read_csv(CSV_REGS):
            self.regs[r['registrationID']] = Registration(r['registrationID'], r['classID'], r['mssv'])
        # debts
        self.debts.clear()
        for r in _read_csv(CSV_DEBTS):
            self.debts[r['DebtID']] = DebtRecord(r['DebtID'], int(r['Debt']))
        # fill students list in each class
        for cl in self.classes.values() :
            cl.setStudent([rg.mssv for rg in self.regs if rg.courseClassID==cl.classID])

    # Saves
    # username,password,fullname,role,email,address,major,compeletedCourse,debtID
    def save_students(self):
        rows = [{
            'mssv':s.getUsername,'password':s.getPass,'fullname':s.getName,'role':s.getRole,
            'email':s.getEmail,'address':s.getAddress,'major':s.getMajor,
            'completedCourse':'|'.join(s.getCompletedCourse),'DebtID':s.getDebtID
        } for s in self.students.values()]
        rows.extend([{
            'username':s.getAdminID,'password':s.getPass,'fullname':s.getName,'role':s.getRole,
            'email':s.getEmail,'address':s.getAddress} for s in self.admin.values()])
        _write_csv(CSV_STUDENTS, rows, ['username','password','fullname','role','email','address','major','completedCourse','DebtID'])

    def save_courses(self):
        rows = [{'courseID':c.courseID,'courseName':c.courseName,'credit':c.credits,'prereq':'|'.join(c.prerequisites)} for c in self.courses.values()]
        _write_csv(CSV_COURSES, rows, ['courseID','courseName','credit','prereq'])

    def save_schedules(self):
        rows = [{'scheduleID':s.scheduleID,'dateStart':s.dateStart,'dateEnd':s.dateEnd,'session':s.session,'dayOfWeek':s.dayOfWeek} for s in self.schedules.values()]
        _write_csv(CSV_SCHEDULES, rows, ['scheduleID','dateStart','dateEnd','session','dayOfWeek'])

    def save_classes(self):
        rows = [{'classID':cl.classID,'courseID':cl.getCourseID,'roomID':cl.getRoomID,'scheduleID':cl.getScheduleID,'maxStudent':cl.getMaxStudents,'status':cl.getStatus} for cl in self.classes.values()]
        _write_csv(CSV_CLASSES, rows, ['classID','courseID','roomID','scheduleID','maxStudent','status'])
    def save_regs(self):
        rows = [{'registrationID':r.registrationID,'mssv':r.mssv,'classID':r.courseClassID} for r in self.regs if r.registrationStatus=='active']
        _write_csv(CSV_REGS, rows, ['registrationID','mssv','classID'])

    def save_debts(self):
        rows = [{'DebtID':d.getDebtID,'debt':d.getDebt} for d in self.debts.values()]
        _write_csv(CSV_DEBTS, rows, ['DebtID','Debt'])

    # Helpers
    def recalc_debt(self, mssv: str, per_credit: int = 500000):
        total = 0
        for r in self.regs:
            if r.mssv==mssv and r.registrationStatus=='active':
                total += self.classes[r.courseClassID].getCredits()
        debt_value = total * per_credit
        self.debts[mssv] = DebtRecord(mssv, debt_value)
        self.save_debts()
        return debt_value
