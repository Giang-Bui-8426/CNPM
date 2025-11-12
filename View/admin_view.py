from tkinter import ttk, messagebox
import customtkinter as ctk


class AdminHome(ctk.CTkFrame):
    def __init__(self,app):
        super().__init__(app)
        self.app = app
        self.pack(fill='both', expand=True)
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self); header.pack(fill='x', padx=8, pady=8)
        ctk.CTkLabel(
            header, text='Admin — Course Register System',
            font=ctk.CTkFont(size=24, weight='bold')
        ).pack(side='left')
        ctk.CTkButton(header, text='Sign out', command=self.app.sign_out).pack(side='right', padx=6)

        upper = ctk.CTkFrame(self); upper.pack(fill='both', expand=True, padx=8, pady=(0,8))
        upper.grid_rowconfigure(0, weight=1)
        upper.grid_columnconfigure(0, weight=1)
        upper.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(upper); left.grid(row=0, column=0, sticky='nsew', padx=(0,8))
        ctk.CTkLabel(left, text='Course', font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(8,4))

        #frame course
        course_cols = ('courseID','courseName','credits','prereq')
        self.tree_course = ttk.Treeview(left, columns=course_cols, show='headings', height=10)
        for c in course_cols:
            self.tree_course.heading(c, text=c)
            self.tree_course.column(c, width=160 if c != 'prereq' else 220, anchor='w')
        self.tree_course.pack(fill='both', expand=True, padx=6, pady=(0,6))
        self.tree_course.bind('<<TreeviewSelect>>', self._clickCourse)

        cbtns = ctk.CTkFrame(left); cbtns.pack(fill='x', padx=6, pady=(0,8))
        ctk.CTkButton(cbtns, text='Add Course', command=self._addCourse).pack(side='left', padx=4)
        ctk.CTkButton(cbtns, text='Delete Course', fg_color='#ef5350', command=self._deleteCourse).pack(side='left', padx=4)
        ctk.CTkButton(cbtns, text='Reload', command=self._refreshCourses).pack(side='left', padx=4)

        # section
        right = ctk.CTkFrame(upper); right.grid(row=0, column=1, sticky='nsew', padx=(8,0))
        right.grid_rowconfigure(1, weight=1)

        self.class_title = ctk.CTkLabel(right, text='Classes (select a course)',
                                        font=ctk.CTkFont(size=18, weight='bold'))
        self.class_title.grid(row=0, column=0, sticky='w', padx=8, pady=(8,4))

        #frame class
        class_cols = ('classID','roomID','session','startDate','endDate','maxStudent','status')
        self.tree_class = ttk.Treeview(right, columns=class_cols, show='headings', height=10)
        for c in class_cols:
            self.tree_class.heading(c, text=c)
            self.tree_class.column(c, width=120, anchor='w')
        self.tree_class.grid(row=1, column=0, sticky='nsew', padx=8, pady=(0,6))
        # khi chọn lớp -> nạp danh sách SV bên dưới
        self.tree_class.bind('<<TreeviewSelect>>', self._clickClass)

        cbtns2 = ctk.CTkFrame(right); cbtns2.grid(row=2, column=0, sticky='w', padx=8, pady=(0,8))
        ctk.CTkButton(cbtns2, text='Add Class', command=self._addClass).pack(side='left', padx=4)
        ctk.CTkButton(cbtns2, text='Delete Class', fg_color='#ef5350', command=self._deleteClass).pack(side='left', padx=4)
        ctk.CTkButton(cbtns2, text='Lock/Unlock', command=self._clickLooked).pack(side='left', padx=4)

        lower = ctk.CTkFrame(self); lower.pack(fill='x', padx=8, pady=(0,8))
        lower.grid_columnconfigure(0, weight=1)
        lower.grid_columnconfigure(1, weight=1)

        # Frame create account
        add_user = ctk.CTkFrame(lower); add_user.grid(row=0, column=0, sticky='nsew', padx=(0,8))
        ctk.CTkLabel(add_user, text='Create Account', text_color='#2e7d32',
                     font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(8,6))
        self.e_mssv = ctk.CTkEntry(add_user, placeholder_text='Start with SV and the size of the following sequence must be greater than 3'); self.e_mssv.pack(fill='x', padx=6, pady=3)
        self.e_full = ctk.CTkEntry(add_user, placeholder_text='Enter fullname'); self.e_full.pack(fill='x', padx=6, pady=3)
        self.e_pwd  = ctk.CTkEntry(add_user, placeholder_text='Enter password ( 6 <= pass size < 50)', show='*'); self.e_pwd.pack(fill='x', padx=6, pady=3)
        self.e_email= ctk.CTkEntry(add_user, placeholder_text='Enter email'); self.e_email.pack(fill='x', padx=6, pady=3)
        self.e_addr = ctk.CTkEntry(add_user, placeholder_text='Enter address'); self.e_addr.pack(fill='x', padx=6, pady=3)
        self.e_major= ctk.CTkEntry(add_user, placeholder_text='Enter major'); self.e_major.pack(fill='x', padx=6, pady=3)
        self.completed = ctk.CTkEntry(add_user, placeholder_text='Enter C001 if only 1 or C000,C002 if 2 or more'); self.completed.pack(fill='x', padx=6, pady=3)
        ctk.CTkButton(add_user, text='Confirm', command=self._createStudent).pack(anchor='e', padx=6, pady=8)

        # Frame student
        stu_box = ctk.CTkFrame(lower); stu_box.grid(row=0, column=1, sticky='nsew', padx=(8,0))
        self.stu_title = ctk.CTkLabel(stu_box, text='Danh sách sinh viên của lớp : (chưa chọn)',
                                      font=ctk.CTkFont(size=18, weight='bold'))
        self.stu_title.pack(pady=(8,6), anchor='w')

        tv_wrap = ctk.CTkFrame(stu_box); tv_wrap.pack(fill='both', expand=True, padx=6)
        self.tree_stu = ttk.Treeview(tv_wrap, columns=('studentID','name'), show='headings', height=6)
        self.tree_stu.heading('studentID', text='Student ID'); self.tree_stu.column('studentID', width=140, anchor='center')
        self.tree_stu.heading('name', text='Name'); self.tree_stu.column('name', width=220, anchor='w')
        yscroll = ttk.Scrollbar(tv_wrap, orient='vertical', command=self.tree_stu.yview)
        self.tree_stu.configure(yscrollcommand=yscroll.set)
        self.tree_stu.grid(row=0, column=0, sticky='nsew')
        yscroll.grid(row=0, column=1, sticky='ns')
        tv_wrap.grid_rowconfigure(0, weight=1); tv_wrap.grid_columnconfigure(0, weight=1)

        # input + buttons -> frame student
        stbtn = ctk.CTkFrame(stu_box); stbtn.pack(fill='x', pady=6, padx=6)
        self.e_stu = ctk.CTkEntry(stbtn, placeholder_text='Enter StudentID'); self.e_stu.pack(side='left', padx=5)
        ctk.CTkButton(stbtn, text='Add Student', command=self._addStudentInClass).pack(side='left', padx=5)
        ctk.CTkButton(stbtn, text='Delete Student', fg_color='#ef5350', command=self._removeStudentOutClass).pack(side='left', padx=5)

        # initial load
        self._refreshCourses()
        self._refreshClasses(None)
        self._refreshStudents(None)

    # load courses {"courseID": cid,"name":name,"credit":credit,"prerequisites":", ".join(prereq)}
    def _refreshCourses(self):
        self.tree_course.delete(*self.tree_course.get_children())
        for row in self.app.read_data.allCourses().values():
            self.tree_course.insert('', 'end', 
                                    values=(row["courseID"], row["name"], row["credit"], row["prerequisites"]))
    # bắt click course
    def _clickCourse(self, _evt):
        sel = self.tree_course.selection()
        course_id = self.tree_course.item(sel[0], 'values')[0] if sel else None
        self._refreshClasses(course_id)
        # reset student list until a class is selected
        self._refreshStudents(None)

    # load class khi chọn lớp
    def _refreshClasses(self, course_id):
        self.tree_class.delete(*self.tree_class.get_children())
        if not course_id:
            self.class_title.configure(text='Classes (select a course)')
            return
        self.class_title.configure(text=f'Classes for Course {course_id}')
        for row in self.app.read_data.getClasses(course_id).values():
            self.tree_class.insert('', 'end', values=(
                row["classID"], row["roomID"], row["session"],
                row["dateStart"], row["dateEnd"], row["maxStudents"], row["status"]
            ))
    # bắt click chọn course
    def _clickClass(self,_evt):
        sel = self.tree_class.selection()
        class_id = self.tree_class.item(sel[0], 'values')[0] if sel else None
        self._refreshStudents(class_id)
        
    # load student
    def _refreshStudents(self, class_id):
        if not class_id:
            return
        for i in self.tree_stu.get_children():
            self.tree_stu.delete(i)
        self.stu_title.configure(
            text=f'List student in class : {class_id}' if class_id else 'List student'
        )
        students = self.app.read_data.studentsInClass(class_id).values()
        for st in students:
            self.tree_stu.insert('', 'end', values=(st[0], st[1]))


    def _addCourse(self):
        win = ctk.CTkToplevel(self); win.title('Add Course'); win.geometry('720x280')
        
        win.transient(self)
        win.grab_set()
        
        def row(lbl,note=''):
            fr=ctk.CTkFrame(win); fr.pack(fill='x', padx=12, pady=6)
            ctk.CTkLabel(fr, text=lbl, width=120).pack(side='left')
            e=ctk.CTkEntry(fr,placeholder_text=note); e.pack(side='left', fill='x', expand=True); return e
        e_id=row('Course ID','Start with C and the number sequence must be greater than 3. Example: C003') 
        e_name=row('Course Name','Enter course name'); e_cr=row('Credits','Enter number credit')
        e_pr=row('Prerequisites','Enter courseID if there are 2 or more, use , to separate (eg: C003, C002)')
        def add():
            cid=e_id.get().strip(); name=e_name.get().strip(); cr=e_cr.get().strip(); pr=e_pr.get().strip()
            if not (cid and name and cr):
                messagebox.showerror("Add Course","Please fill in all information in the field.")
                return
            check,tmp = self.app.courses_manage.addCourse(cid,name,[p for p in pr.split(',') if p], cr)
            if not check:
                messagebox.showerror('Add Course',tmp); return
            messagebox.showinfo('Add Course','Add course successively')
            self._refreshCourses(); win.destroy()
        ctk.CTkButton(win, text='Create', command=add).pack(pady=8)

    def _deleteCourse(self):
        sel = self.tree_course.selection()
        if not sel: return
        cid = self.tree_course.item(sel[0],'values')[0]
        if self.app.read_data.checkCourseHasClass(cid):
            messagebox.showerror('Delete','Cannot delete course because class is open'); return
        if not self.app.courses_manage.removeCourse(cid):
            messagebox.showerror("Delete","CourseID no exists")
        self._refreshCourses()

    def _addClass(self):
        sel = self.tree_course.selection()
        if not sel:
            messagebox.showwarning('Add Class','Select a course first'); return
        course_id = self.tree_course.item(sel[0],'values')[0]

        win = ctk.CTkToplevel(self); win.title(f'Add Class for {course_id}'); win.geometry('720x420')
        win.transient(self)
        win.grab_set()
        
        def row(lbl,note=''):
            fr=ctk.CTkFrame(win); fr.pack(fill='x', padx=12, pady=6)
            ctk.CTkLabel(fr, text=lbl, width=160).pack(side='left')
            e=ctk.CTkEntry(fr,placeholder_text=note); e.pack(side='left', fill='x', expand=True); return e
        e_id=row('Class ID',"Start with CL and the number sequence must be greater than 3. Example: CL003")
        e_room=row('Room ID',"Start with R"); e_day=row('DayOfWeek','Enter (Monday, Thursday,...)')
        e_sess=row('Session','Enter 1-4'); e_start=row('Start Date (dd/mm/yyyy)','Enter in required format Example: 12/12/2025')
        e_end=row('End Date (dd/mm/yyyy)','Enter in required format Example: 12/12/2025')
        e_max=row('Max Students','Enter number')

        def add():
            cid=e_id.get().strip(); room=e_room.get().strip(); day=e_day.get().strip()
            sess=e_sess.get().strip(); st=e_start.get().strip(); en=e_end.get().strip(); m=e_max.get().strip()
            if not (cid and room and day and sess and st and en and m):
                messagebox.showerror("Add Course","Please fill in all information in the field.")
                return
            check,sched = self.app.courses_manage.addSchedule(st, en, sess, day)
            if not check:
                messagebox.showerror("Schedule",sched); return
            checkC,tmp = self.app.courses_manage.addCourseClass(cid,course_id,room,m,sched)
            if not checkC:
                messagebox.showerror('Add',tmp); return
            messagebox.showinfo("","Add class successively")
            self._refreshClasses(course_id); win.destroy()
        ctk.CTkButton(win, text='Create', command=add).pack(pady=8)

    def _deleteClass(self):
        selc = self.tree_class.selection(); selco= self.tree_course.selection()
        if not selc or not selco: return
        cid = self.tree_class.item(selc[0],'values')[0]
        course_id = self.tree_course.item(selco[0],'values')[0]
        check,tmp = self.app.courses_manage.removeCourseClass(cid)
        if not check:
            messagebox.showwarning("delete class",tmp)
            return
        self._refreshClasses(course_id)

    # button trạng thái lớp
    def _clickLooked(self):
        selc = self.tree_class.selection(); 
        cid = self.tree_class.item(selc[0],'values')[0]
        selco = self.tree_course.selection()
        clid = self.tree_course.item(selco[0],'values')[0]
        self.app.courses_manage.lookedStatus(cid)
        self._refreshClasses(clid)

    def _addStudentInClass(self):
        sel = self.tree_class.selection()
        if not sel:
            messagebox.showwarning('Add Student','Please select class'); return
        class_id = self.tree_class.item(sel[0], 'values')[0]
        mssv = self.e_stu.get().strip()
        if not mssv:
            messagebox.showwarning('Add Student','Enter studentID'); return
        
        check,tmp = self.app.reg_ctrl.register(mssv, class_id,True)
        if not check: messagebox.showerror('Add Student', tmp); return
        self.e_stu.delete(0, 'end')
        messagebox.showinfo("Add Student",'Add Student Successively')
        self._refreshStudents(class_id)

    def _removeStudentOutClass(self):
        sel = self.tree_class.selection()
        if not sel:
            messagebox.showwarning('Delete Student','Please select class'); return
        class_id = self.tree_class.item(sel[0], 'values')[0]

        sel_stu = self.tree_stu.selection()
        if not sel_stu:
            messagebox.showwarning('Delete Student','Please select student'); return
        mssv = self.tree_stu.item(sel_stu[0], 'values')[0]

        check,tmp = self.app.reg_ctrl.cancelRegister(mssv,class_id,True)
        if not check:
            messagebox.showwarning("Remove register",tmp)
            return
        messagebox.showinfo("Remove","Kick students successively")
        self._refreshStudents(class_id)

    def _createStudent(self):
        mssv = self.e_mssv.get().strip()
        Pass = self.e_pwd.get().strip()
        full=self.e_full.get().strip(); email=self.e_email.get().strip()
        addr=self.e_addr.get().strip(); major=self.e_major.get().strip()
        comp = list(self.completed.get().strip().split(","))
        if not mssv or not full or not email or not addr or not major:
            messagebox.showerror('Create Student','Please enter complete information'); return
        check,tmp = self.app.account_ctrl.createAccount(mssv,Pass,full,email,addr,major,comp)
        if not check:
            messagebox.showerror("Create Account",tmp)
            return
        messagebox.showinfo('Create Student', 'Account created successfully')
        for e in [self.e_mssv,self.e_pwd,self.e_full,self.e_email,self.e_addr,self.e_major,self.completed]:
            e.delete(0,'end')
