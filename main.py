
import customtkinter as ctk
from repository import Repository
from controllers.courseController import CourseController
from controllers.registerController import RegisterController
from controllers.accountController import AccountController
from controllers.readDataController import ReadDataController
from View.login_view import LoginView
from View.student_view import StudentView
from View.profile_view import ProfileView
from View.change_pass import ChangePasswordView
from View.registered_view import RegisteredCoursesView
from View.schedule_view import ScheduleView
from View.admin_view import AdminHome

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('light'); ctk.set_default_color_theme('green')
        self.title('Course Registration'); self.geometry('1200x750')
        self.repo = Repository(); self.repo.load()
        self.read_data = ReadDataController(self.repo)
        self.reg_ctrl = RegisterController(self.repo)
        self.courses_manage = CourseController(self.repo)
        self.account_ctrl = AccountController(self.repo)
        self.current_user=None
        self.current_role=None
        self.show_login()
    def clear(self):
        for w in self.winfo_children(): w.destroy()
    def show_login(self):
        self.clear(); LoginView(self)
    def show_student(self):
        self.clear(); StudentView(self).pack(fill='both', expand=True)
    def show_profile(self):
        self.clear(); ProfileView(self).pack(fill='both', expand=True)
    def show_change_pass(self):
        self.clear(); ChangePasswordView(self).pack(fill='both', expand=True)
    def show_registered(self):
        self.clear(); RegisteredCoursesView(self).pack(fill='both', expand=True)
    def show_schedule(self):
        self.clear(); ScheduleView(self).pack(fill='both', expand=True)
    def show_admin(self):
        self.clear(); AdminHome(self)
    def sign_out(self):
        self.current_user=None
        self.current_role=None; self.show_login()

if __name__ == '__main__':
    App().mainloop()
