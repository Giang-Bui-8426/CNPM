# readDataController.py
from typing import Dict, List, Tuple

class ReadDataController:
    def __init__(self, repo, course_ctrl=None, reg_ctrl=None, account_ctrl=None):
        self.repo = repo
        self.course_ctrl = course_ctrl
        self.reg_ctrl = reg_ctrl
        self.account_ctrl = account_ctrl

    # return dict information student
    def student_profile(self, mssv) :
        s = self.repo.students[mssv]
        debt_id = s.debtID
        debt_val = 0
        if debt_id and debt_id in self.repo.debts:
            debt_val = self.repo.debts[debt_id].debt
        return {
            "mssv": s.mssv,
            "name": s.name,
            "email": s.email,
            "major": s.major,
            "address": s.address,
            "debt": debt_val,
        }
    # return course sv có thể đăng ký
    def getcourses(self,mssv):
        listCourse = []
        registeringCourse = list(self.repo.classes[r.classID].courseID for r in self.repo.regs if r.mssv == mssv and r.status == "active")
        compeletedCourse = self.repo.students[mssv].completedCourse
        for c in self.repo.courses.values():
            if c.courseID not in compeletedCourse and c.courseID not in registeringCourse:
                tmp = True
                if c.prerequisites:
                    for p in c.prerequisites:
                        if p not in compeletedCourse:
                            tmp = False 
                            break
                if tmp:
                    listCourse.append(c)
        return listCourse
    
    # return information các course mà student có thể đăng ký
    def getCourses(self, mssv):
        course = self.getcourses(mssv)
        rows = {}
        for c in course:
            cid = c.courseID
            name = c.courseName
            credit = c.credit
            prereq = c.prerequisites
            rows[cid] = {"courseID": cid,"name":name,"credit":credit,"prerequisites":", ".join(prereq)}
        return rows
    #return list all courses
    def allCourses(self):
        rows = {}
        for c in self.repo.courses.values():
            cid = c.courseID
            name = c.courseName
            credit = c.credit
            prereq = c.prerequisites
            rows[cid] = {"courseID": cid,"name":name,"credit":credit,"prerequisites":", ".join(prereq)}
        return rows
    #return các class với course tương ứng
    def getClasses(self,courseID):
        rows = {}
        for cl in self.repo.classes.values():
            if cl.courseID == courseID:
                rows["classID"] = self.getClass(cl.classID)
        return rows
    
    # ktr xem course có class nào không 
    def checkCourseHasClass(self, course_id):
        for cl in self.repo.classes.values():
            if cl.courseID == course_id:
                return True
        return False

    # return dict (classID, roomID, dayOfWeek, session, dateStart, dateEnd, maxStudent, status)
    def classes_table_rows(self, course_id):
        rows = {}
        for cl in self.repo.classes.values():
            cid = cl.courseID
            if cid != course_id:
                continue
            sch = self.repo.schedules[cl.scheduleID]
            day = sch.dayOfWeek
            session = int(sch.session)
            date_start = sch.dateStart
            date_end = sch.dateEnd
            max_st = int(cl.maxStudent)
            status = cl.status

            rows[cl.classID] = [cl.classID, cl.roomID, day,session, date_start, date_end, max_st, status]
        return rows

    # return số lượng sinh viên đăng ký ở lớp
    def countEnrolledInClass(self, class_id):
        active = 0
        for r in self.repo.regs:
            status = r.status
            if r.classID == class_id and status == "active":
                active += 1
        return active

    
    def studentsInClass(self, class_id):
        rows = {}
        for r in self.repo.regs:
            if r.classID == class_id and r.status == "active":
                mssv = r.mssv
                full = self.repo.students[mssv].name
                rows[mssv] = [mssv, full]
        return rows

    #return detail information về class
    def getClass(self, class_id):
        cl = self.repo.classes[class_id]
        sch = self.repo.schedules[cl.scheduleID]
        day = sch.dayOfWeek
        sess = int(sch.session)
        return {"classID" :class_id,"session":f"{sess} - {day}","dayOfWeek" : day,"dateStart":sch.dateStart,
                "dateEnd":sch.dateEnd,"roomID": cl.roomID,
                "status":cl.status,"maxStudents":cl.maxStudents}

    # return detail information  về regs bao gồm tổng credit , debt của 1 sv
    #(classID, courseName, credit, scheduleText, lockStatus)
    def listRegistered(self, mssv):
        rows, total = [], 0
        for r in self.repo.regs:
            if r.mssv != mssv or r.status != "active":
                continue
            cl = self.repo.classes[r.classID]
            co = self.repo.courses[cl.courseID]
            sch = self.repo.schedules[cl.scheduleID]
            
            sched_text = (f"Session {sch.session} - "
                          f"{sch.dayOfWeek},"
                          f"{sch.dateStart} - {sch.dateEnd}")
            rows.append([cl.classID, co.courseName, int(co.credit),
                         sched_text, ("Not locked yet" if cl.status=="open" else "Locked")])
            total += int(co.credit)

        return rows, total

    # return information cho schedule
    def schedule(self, mssv):
        cells = {}
        for r in self.repo.regs:
            if r.mssv != mssv or r.status != "active":
                continue
            cl = self.repo.classes[r.classID]
            co = self.repo.courses[cl.courseID]
            sch = self.repo.schedules[cl.scheduleID]
            
            day = sch.dayOfWeek
            sess = int(sch.session)
            cells[(sess, day)] = f"{co.courseName}\n{sch.dateStart} - {sch.dateEnd}\nRoom: {cl.roomID}"
        return cells
