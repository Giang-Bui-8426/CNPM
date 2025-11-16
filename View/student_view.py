import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import re

class StudentView(ctk.CTkFrame):
    def __init__(self,app):
        super().__init__(app); self.app=app
        self.grid_rowconfigure(0, weight=1); self.grid_columnconfigure(1, weight=1)
        self._build()

    def _build(self):
        sidebar = ctk.CTkFrame(self, width=220)
        sidebar.grid(row=0, column=0, sticky='nsw', padx=(8,0), pady=8)
        sidebar.grid_propagate(False)
        #Frame right
        ctk.CTkLabel(sidebar, text=self.app.read_data.student_profile(self.app.current_user)["name"], font=ctk.CTkFont(size=18, weight='bold')).pack(pady=(12,8))
        ctk.CTkButton(sidebar, text='Student profile',  command=self.app.show_profile).pack(fill='x', padx=12, pady=6)
        ctk.CTkButton(sidebar, text='Change Password', command=self.app.show_change_pass).pack(fill='x', padx=12, pady=6)
        ctk.CTkButton(sidebar, text='My Course',       command=self.app.show_registered).pack(fill='x', padx=12, pady=6)
        ctk.CTkButton(sidebar, text='Schedule',        command=self.app.show_schedule).pack(fill='x', padx=12, pady=6)
        ctk.CTkButton(sidebar, text='Sign Out',        command=self.app.sign_out, fg_color='#ef5350').pack(fill='x', padx=12, pady=12)

        main = ctk.CTkFrame(self)
        main.grid(row=0, column=1, sticky='nsew', padx=8, pady=8)
        main.grid_rowconfigure(2, weight=1); main.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(main, text='Course Register System',
                     font=ctk.CTkFont(size=22, weight='bold')).grid(row=0, column=0, columnspan=3, pady=(6,4))

        # Frame Courses
        area = ctk.CTkFrame(main); area.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=(8,6), pady=6)
        area.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(area, text='Search :').grid(row=0, column=0, padx=8, pady=6, sticky='e')
        self.courseEntry = tk.StringVar()
        ctk.CTkEntry(area, textvariable=self.courseEntry, placeholder_text='Enter name subject').grid(row=0, column=1, sticky='ew', padx=(0,6), pady=6)
        ctk.CTkButton(area, text='OK', width=42, command=self.refreshCourse).grid(row=0, column=2, padx=6, pady=6)

        cols=('CourseID','Subject','Credit','Prerequisites','Information')
        self.tree = ttk.Treeview(area, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150 if c!='Prerequisites' else 220, anchor='w')
        self.tree.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=8, pady=(2,8))
        self.tree.bind('<Button-1>', self._click)

        ## Frame classes
        right = ctk.CTkFrame(main); right.grid(row=1, column=2, sticky='ns', padx=(0,8), pady=6)
        ctk.CTkLabel(right, text='Class', fg_color='#e53935', text_color='white',
                     corner_radius=8, width=240).pack(padx=6, pady=(4,6))
        
        self.classList = ctk.CTkScrollableFrame(right, width=260, height=310)
        self.classList.pack(padx=6, pady=(0,8), fill='both', expand=False)

        # Search class
        en = ctk.CTkFrame(right); en.pack(fill='x', padx=6, pady=(0,6))
        ctk.CTkLabel(en, text='Enter classID').pack(side='left', padx=6)
        self.classEntry = tk.StringVar()
        ctk.CTkEntry(en, textvariable=self.classEntry, width=120).pack(side='left', padx=4)
        self.button_class = ctk.CTkButton(en, text='OK', width=42)
        self.button_class.pack(side="left",padx=4)
        # frame detail class
        self.detailFrame = ctk.CTkFrame(right, corner_radius=10, fg_color='#c8e6c9')
        self.detailFrame.pack(fill='x', padx=6, pady=(0,8))
        self.detailTitle = ctk.CTkLabel(self.detailFrame, text='Detail of class',
                                         text_color='#1b5e20', font=ctk.CTkFont(size=16, weight='bold'))
        self.detailTitle.pack(anchor='w', padx=10, pady=(8,4))
        self.detailText  = ctk.CTkLabel(self.detailFrame, text='', justify='left', anchor='w', text_color='#1b5e20')
        self.detailText.pack(fill='x', padx=10, pady=(0,10))

        # Register button (near the right panel)
        self.buttonRegis = ctk.CTkButton(right, text='Register', command=self.excuteRegister)
        self.buttonRegis.pack(padx=6, pady=4)

        self.refreshCourse()

    # load subject lên interface
    # q là namesubject do ngdung nhập , nếu có thì khi duyệt những môn không giống q sẽ không được show
    # hàm này lọc course để hiển thị course thỏa đk hiển thị thứ tự tên lớp và prerequisites 
    def refreshCourse(self):
        self.tree.delete(*self.tree.get_children())
        q = (self.courseEntry.get() or '').lower()

        # sort subject theo name
        courses = list(self.app.read_data.getCourses(self.app.current_user).values())
        courses.sort(key=lambda c: (c["name"] or '').lower())

        for co in courses:
            if q and q not in (co["name"] or '').lower(): 
                continue
            prereq = co["prerequisites"] if co["prerequisites"] else ""
            self.tree.insert('', 'end', values=(co["courseID"], co["name"], co["credit"], prereq, 'Detail'))

        # reset danh sách lớp
        for w in self.classList.winfo_children(): w.destroy()
        self.detailTitle.configure(text='Detail of class')
        self.detailText.configure(text='')
        self.classEntry.set('')

    # bắt click
    def _click(self, event):
        item = self.tree.identify_row(event.y)
        col  = self.tree.identify_column(event.x)
        if not item: return
        if col == '#5':
            course_id = self.tree.item(item, 'values')[0]
            self.button_class.configure(command=lambda cid=course_id: self.showClass(cid,self.classEntry.get().strip()))
            self.showClass(course_id)
    # show class
    def showClass(self, course_id,classID = None):

        for w in self.classList.winfo_children(): w.destroy()
        classes = list(self.app.read_data.getClasses(course_id).values())
        if not classes:
            ctk.CTkLabel(self.classList, text='No classes for this course').pack(pady=12)
            return
        if classID:
            cls = self.app.read_data.getClass(classID)
            if cls in classes:
                classes = [cls]
            else:
                ctk.CTkLabel(self.classList, text="ClassID does not exist").pack(pady=12)
                return      
        # sort theo 3 số cuối mã lớp
        def last3(cls):
            m = re.search(r'(\d{3})$', cls["classID"])
            return int(m[0]) if m else 0
        classes.sort(key=last3)


        for cl in classes:
            enrolled = self.app.reg_ctrl.amountStudentInClass(cl["classID"])
            cap = f"{enrolled}/{cl['maxStudents']}"
            btn = ctk.CTkButton(self.classList, height=56,
                                text=f"{cl['classID']} - {cl['roomID']}\n{cl['session']}  {cap}",
                                command=lambda c=cl : self.detailClass(c))
            btn.pack(fill='x', padx=6, pady=4)

    # Detail of class
    def detailClass(self, cl):
        self.detailTitle.configure(text=f"Detail : {cl['classID']}")
        info = f"""Room : {cl["roomID"]}
                Session {cl["session"]},
                {cl["dateStart"]} - {cl["dateEnd"]}
                """
        self.detailText.configure(text=info)
        self.classEntry.set(cl["classID"])
        return

    # Register
    def excuteRegister(self):
        cid = self.classEntry.get().strip()
        check,tmp = self.app.reg_ctrl.register(self.app.current_user,cid)
        if not check:
            messagebox.showwarning('Register', tmp)
            return
        messagebox.showinfo('Register', 'Register Successively')
        self.refreshCourse()