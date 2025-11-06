
import customtkinter as ctk
from tkinter import messagebox
class ChangePasswordView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master); self.app=app; self._build()
    def _build(self):
        top=ctk.CTkFrame(self); top.pack(fill='x')
        ctk.CTkButton(top, text='← Back', width=100, command=self.app.show_student).pack(side='left', padx=8, pady=8)
        ctk.CTkLabel(top, text='Change Password', font=ctk.CTkFont(size=22, weight='bold')).pack(side='left', pady=8, padx=6)
        def row(label):
            fr=ctk.CTkFrame(self); fr.pack(fill='x', padx=16, pady=6)
            ctk.CTkLabel(fr,text=label,width=160).pack(side='left')
            e=ctk.CTkEntry(fr, show='*'); e.pack(side='left', fill='x', expand=True); return e
        e_old=row('Old Password'); e_new=row('New Password'); e_cf=row('Confirm Password')
        def change():
            if e_new.get()!=e_cf.get(): messagebox.showwarning('Change','Confirm mismatch'); return
            check,tmp = self.app.account_ctrl.changePass(self.app.current_user,e_new.get(),e_old.get())
            if not check:
                messagebox.showerror('Change',tmp); return
            messagebox.showinfo('Change','Changed successfully')
        ctk.CTkButton(self, text='Change', height=40, command=change).pack(pady=8)
