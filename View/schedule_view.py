
import customtkinter as ctk
DAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
class ScheduleView(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master); self.app=app; self._build()
    def _build(self):
        top=ctk.CTkFrame(self); top.pack(fill='x')
        ctk.CTkButton(top, text='← Back', width=100, command=self.app.show_student).pack(side='left', padx=8, pady=8)
        ctk.CTkLabel(top, text='Registered Class Schedule', font=ctk.CTkFont(size=22, weight='bold')).pack(side='left', pady=8, padx=6)
        table=ctk.CTkFrame(self); table.pack(fill='both', expand=True, padx=12, pady=12)
        sessions=[1,2,3,4]
        for r in range(0,len(sessions)+1): table.grid_rowconfigure(r, weight=1, uniform='r')
        for c in range(0,len(DAYS)+1): table.grid_columnconfigure(c, weight=1, uniform='c')
        ctk.CTkLabel(table, text='Day / School shift', fg_color='#79c3df', text_color='white',
                     font=ctk.CTkFont(size=14, weight='bold'), corner_radius=8).grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
        for i,d in enumerate(DAYS, start=1):
            ctk.CTkLabel(table, text=d, fg_color='#79c3df', text_color='white',
                         font=ctk.CTkFont(size=14, weight='bold'), corner_radius=8).grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        # filter lấy những regs đúng của sinh viên 
        schedules=self.app.read_data.schedule(self.app.current_user)
        for r,s in enumerate(sessions, start=1):
            ctk.CTkLabel(table, text=f'Session {s}', fg_color='#e0e0e0', text_color='black',
                         corner_radius=8).grid(row=r, column=0, sticky='nsew', padx=1, pady=1)
            for c,d in enumerate(DAYS, start=1):
                text = schedules.get((s,d),"")
                ctk.CTkLabel(table, text=text, fg_color='#efefef', text_color='black',
                             corner_radius=8, anchor='center', justify='center').grid(row=r, column=c, sticky='nsew', padx=1, pady=1)
