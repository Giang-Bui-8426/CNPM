import customtkinter as ct
from tkinter.messagebox import showinfo, showerror

ct.set_appearance_mode("light")
ct.set_default_color_theme("green")

class ChangePassword(ct.CTk):

    def __init__(self):
        super().__init__()
        self.title("Change Password")
        self.geometry("700x500")

        # TITLE BAR --------------------
        title = ct.CTkLabel(self, text="Change Password",
                            fg_color="#00c38e",
                            text_color="white",
                            corner_radius=10,
                            height=60,
                            font=("Arial", 24, "bold"))
        title.pack(fill="x", pady=10, padx=10)

        # MAIN PANEL -------------------
        box = ct.CTkFrame(self, corner_radius=15)
        box.pack(pady=40, padx=30, fill="x")

        # OLD PASS
        ct.CTkLabel(box, text="Old Password",
                    fg_color="#66e6a3",
                    corner_radius=8,
                    width=150,
                    height=40,
                    font=("Arial", 14, "bold")).grid(row=0, column=0, padx=20, pady=15)

        ct.CTkLabel(box, text=":", font=("Arial", 20)).grid(row=0, column=1)

        self.old_pass = ct.CTkEntry(box, show="*", width=250)
        self.old_pass.grid(row=0, column=2, padx=20)

        # NEW PASS
        ct.CTkLabel(box, text="New Password",
                    fg_color="#66e6a3",
                    corner_radius=8,
                    width=150,
                    height=40,
                    font=("Arial", 14, "bold")).grid(row=1, column=0, padx=20, pady=15)

        ct.CTkLabel(box, text=":", font=("Arial", 20)).grid(row=1, column=1)

        self.new_pass = ct.CTkEntry(box, show="*", width=250)
        self.new_pass.grid(row=1, column=2, padx=20)

        # CONFIRM PASS
        ct.CTkLabel(box, text="Confirm Password",
                    fg_color="#66e6a3",
                    corner_radius=8,
                    width=150,
                    height=40,
                    font=("Arial", 14, "bold")).grid(row=2, column=0, padx=20, pady=15)

        ct.CTkLabel(box, text=":", font=("Arial", 20)).grid(row=2, column=1)

        self.confirm_pass = ct.CTkEntry(box, show="*", width=250)
        self.confirm_pass.grid(row=2, column=2, padx=20)

        # BUTTONS ---------------------
        btn_frame = ct.CTkFrame(self)
        btn_frame.pack(pady=20)

        ct.CTkButton(btn_frame, text="Change", fg_color="green",
                     hover_color="#0d8f5f",
                     width=150, height=40,
                     command=self.change_pwd).grid(row=0, column=0, padx=40)

        ct.CTkButton(btn_frame, text="Cancel", fg_color="red",
                     hover_color="#c23a3a",
                     width=150, height=40,
                     command=self.destroy).grid(row=0, column=1, padx=40)

    # FUNCTION ---------------------
    def change_pwd(self):
        old = self.old_pass.get().strip()
        new = self.new_pass.get().strip()
        confirm = self.confirm_pass.get().strip()

        if old == "" or new == "" or confirm == "":
            showerror("Error", "Fields cannot be empty!")
            return

        if new != confirm:
            showerror("Error", "Password does not match!")
            return

        showinfo("Success", "Password changed successfully!")


if __name__ == "__main__":
    ChangePassword().mainloop()
