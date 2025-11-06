
import customtkinter as ctk
from tkinter import messagebox
class LoginView(ctk.CTkFrame):
    def __init__(self, master, app): # master dùng để làm tham số chứa Frame , app điều khiển luồng 
        super().__init__(master); self.app=app
        self.pack(fill='both', expand=True); self._build()
    def _build(self):
        ctk.CTkLabel(self, text='Course Registration', font=ctk.CTkFont(size=26, weight='bold')).pack(pady=(40,10))
        card = ctk.CTkFrame(self, corner_radius=12); card.pack(pady=10, ipadx=12, ipady=12)
        r1=ctk.CTkFrame(card); r1.pack(padx=16,pady=8,fill='x'); r2=ctk.CTkFrame(card); r2.pack(padx=16,pady=8,fill='x')
        ctk.CTkLabel(r1,text='MSSV/Username',width=160).pack(side='left'); ctk.CTkLabel(r2,text='Password',width=160).pack(side='left')
        self.username=ctk.CTkEntry(r1,width=260); self.username.pack(side='left')
        self.password=ctk.CTkEntry(r2,show='*',width=260); self.password.pack(side='left')
        ctk.CTkButton(self,text='Sign in',command=self._login, height=40).pack(pady=12)
    def _login(self):
        role=self.app.account_ctrl.login(self.username.get().strip(), self.password.get().strip())
        if role:
            self.app.current_user=self.username.get().strip()
            self.app.current_role=role
            if role=='admin': self.app.show_admin()
            else: self.app.show_student()
        else:
            messagebox.showerror('Login','Invalid credentials')
