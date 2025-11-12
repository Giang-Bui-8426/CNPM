
import customtkinter as ctk
from tkinter import ttk, messagebox
class RegisteredCoursesView(ctk.CTkFrame):
    def __init__(self,app):
        super().__init__(app); self.app=app; self._build()
    def _build(self):
        top=ctk.CTkFrame(self); top.pack(fill='x')
        ctk.CTkButton(top, text='← Back', width=100, command=self.app.show_student).pack(side='left', padx=8, pady=8)
        ctk.CTkLabel(top, text='Registered Courses', font=ctk.CTkFont(size=22, weight='bold')).pack(side='left', pady=8, padx=6)
        cols=('ClassID','Subject','Credit','Schedule','Status','Cancel')
        self.tree=ttk.Treeview(self, columns=cols, show='headings', height=12)
        for c in cols: self.tree.heading(c, text=c); self.tree.column(c, width=160, anchor='w')
        self.tree.pack(fill='both', expand=True, padx=12, pady=8)
        self.lbl=ctk.CTkLabel(self, text='Total credits: 0'); self.lbl.pack(pady=4)
        self.debt_lbl=ctk.CTkLabel(self, text='Debt: 0'); self.debt_lbl.pack(pady=4)
        self.refresh(); self.tree.bind('<Button-1>', self._on_click)
    #load thông tin
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        rows,total = self.app.read_data.listRegistered(self.app.current_user)
        for r in rows: 
            self.tree.insert('', 'end', values=(r[0], r[1], r[2], r[3], r[4], 'Cancel'))
        self.lbl.configure(text=f'Total credits: {total}')
        debt = self.app.reg_ctrl.recalc_debt(self.app.current_user)
        self.debt_lbl.configure(text=f'Debt: {debt:,} VND')
    def _on_click(self, event):
        # item bắt vị trí hàng , col bắt vị trí cột -- khi click vào table
        item=self.tree.identify_row(event.y); col=self.tree.identify_column(event.x)
        if not item: return
        vals=self.tree.item(item,'values')
        if col=='#6':
            confirm = messagebox.askokcancel("Cancel","Are you sure you want to cancel?")
            if confirm:
                check,tmp = self.app.reg_ctrl.cancelRegister(self.app.current_user, vals[0])
                if check:
                    messagebox.showinfo("inform","Cancel success")
                    self.refresh()
                else:
                    messagebox.showwarning("inform",tmp)
