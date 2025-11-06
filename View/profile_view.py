
import customtkinter as ctk
from tkinter import messagebox
class ProfileView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master); self.app=app; self._build()
    def _build(self):
        top=ctk.CTkFrame(self); top.pack(fill='x')
        ctk.CTkButton(top, text='← Back', width=100, command=self.app.show_student).pack(side='left', padx=8, pady=8)
        ctk.CTkLabel(top, text='Student Profile', font=ctk.CTkFont(size=22, weight='bold')).pack(side='left', pady=8, padx=6)
        s = self.app.read_data.student_profile(self.app.current_user)
        form = ctk.CTkFrame(self, corner_radius=10); form.pack(padx=16, pady=12, fill='x')
        self.entries={}
        def row(label,key,disabled=False):
            fr=ctk.CTkFrame(form); fr.pack(fill='x', padx=12, pady=6)
            ctk.CTkLabel(fr, text=label, width=140).pack(side='left')
            e=ctk.CTkEntry(fr); e.insert(0,s[key])
            if disabled: e.configure(state='disabled')
            e.pack(side='left', fill='x', expand=True); self.entries[key]=e
        row('Student ID','mssv',True); row('Full Name','name'); row('Email','email')
        row('Major','major'); row('Address','address')
        def save():
            check,error = self.app.account_ctrl.updateProfile(self.app.current_user,
                name=self.entries['name'].get().strip(),
                email=self.entries['email'].get().strip(),
                major=self.entries['major'].get().strip(),
                address=self.entries['address'].get().strip(),
            )
            if not check:
                messagebox.showwarning('Profile',error)
            else:
                messagebox.showinfo('Profile','Saved success')
        ctk.CTkButton(self, text='Save', command=save).pack(pady=6)
