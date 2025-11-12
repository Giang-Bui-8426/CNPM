import customtkinter as ct
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror

# DATA --------------
COURSES = [
    {"id": "C01", "subject": "Software Technology", "credit": 3, "prereq": "C00"},
    {"id": "C02", "subject": "Database System", "credit": 3, "prereq": "C00"},
    {"id": "C03", "subject": "Computer Networks", "credit": 3, "prereq": "C01"},
]

CLASSES = [
    {"class": "CL02 - R01", "cap": "2/30",
     "detail": "Room: R01\nSession: Friday\n21/09/2025 - 30/12/2025"},
    {"class": "CL03 - R02", "cap": "15/30",
     "detail": "Room: R02\nSession: Monday\n21/09/2025 - 30/12/2025"},
]

ct.set_appearance_mode("light")
ct.set_default_color_theme("green")

class App(ct.CTk):

    def __init__(self):
        super().__init__()
        self.title("Course Register System")
        self.geometry("1200x700")

        # Layout configs
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- LEFT SIDEBAR ----------------
        left = ct.CTkFrame(self, width=200, corner_radius=0)
        left.grid(row=0, column=0, sticky="ns")

        ct.CTkLabel(left, text="Name Student",
                    font=("Arial", 18, "bold")).pack(pady=20)

        for name in ["Student profile", "Change Password",
                     "My Course", "Schedule", "Sign Out"]:
            ct.CTkButton(left, text=name,
                         fg_color="red" if name == "Sign Out" else "green").pack(
                pady=10, fill="x"
            )

        # ---------------- CENTER PANEL ----------------
        center = ct.CTkFrame(self, corner_radius=15)
        center.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        center.grid_columnconfigure(0, weight=1)

        ct.CTkLabel(center, text="Course Register System",
                    font=("Arial", 24, "bold")).pack(pady=10)

        # Search box
        search_frame = ct.CTkFrame(center)
        search_frame.pack(pady=10, fill="x")

        ct.CTkLabel(search_frame, text="Search :").pack(side="left", padx=10)

        self.search_entry = ct.CTkEntry(search_frame, placeholder_text="Enter name subject")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_course)

        # Table ----------------
        self.table = ttk.Treeview(center, columns=("id", "sub", "cre", "pre", "info"),
                                  show="headings", height=12)
        self.table.pack(fill="both", expand=True, pady=10)

        for col, text in zip(("id", "sub", "cre", "pre", "info"),
                             ("CourseID", "Subject", "Credit", "Prereq", "Information")):
            self.table.heading(col, text=text)
            self.table.column(col, width=120)

        self.populate_table()

        ct.CTkButton(center, text="OK", width=100).pack(pady=10)

        # ---------------- RIGHT PANEL ----------------
        right = ct.CTkFrame(self, width=260, corner_radius=15)
        right.grid(row=0, column=2, sticky="ns", padx=10, pady=15)

        ct.CTkLabel(right, text="Class", fg_color="red",
                    corner_radius=8, font=("Arial", 18, "bold"), width=200).pack(pady=10)

        # Class list
        self.class_list = ct.CTkScrollableFrame(right, width=200, height=300)
        self.class_list.pack(pady=10, fill="x")

        for cl in CLASSES:
            ct.CTkButton(
                self.class_list,
                text=f"{cl['class']} ({cl['cap']})",
                fg_color="#8ef5a3",
                text_color="black",
                hover_color="#69d889",
                command=lambda c=cl: self.show_class_detail(c)
            ).pack(pady=5, fill="x")

        # Class ID entry
        self.class_id = ct.CTkEntry(right, placeholder_text="Enter classID")
        self.class_id.pack(pady=10, fill="x")

        # Detail box
        self.detail_box = ct.CTkTextbox(right, height=150)
        self.detail_box.pack(fill="x", pady=10)

        # Register button
        ct.CTkButton(right, text="Register", fg_color="blue",
                     hover_color="#0a57d5", command=self.register).pack(pady=10)

    # ------------- FUNCTIONS -----------------

    def populate_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for c in COURSES:
            self.table.insert("", "end",
                              values=(c["id"], c["subject"],
                                      c["credit"], c["prereq"], "Detail"))

    def filter_course(self, event=None):
        text = self.search_entry.get().lower()
        self.table.delete(*self.table.get_children())

        for c in COURSES:
            if text in c["subject"].lower() or text in c["id"].lower():
                self.table.insert("", "end",
                                  values=(c["id"], c["subject"],
                                          c["credit"], c["prereq"], "Detail"))

    def show_class_detail(self, cl):
        self.class_id.delete(0, "end")
        self.class_id.insert(0, cl["class"])

        self.detail_box.delete("0.0", "end")
        self.detail_box.insert("0.0", f"Detail: {cl['class']}\n{cl['detail']}")

    def register(self):
        cid = self.class_id.get().strip()

        if cid == "":
            showwarning("Warning", "Please enter Class ID!")
            return

        if cid not in [c["class"] for c in CLASSES]:
            showerror("Error", "Class not found!")
            return

        showinfo("Success", f"Registered to class: {cid}")


if __name__ == "__main__":
    App().mainloop()
