import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My Course Functional Interface")
root.geometry("700x300")

cols = ("ClassID", "Subject", "Credit", "Schedule", "Status", "Action")
tree = ttk.Treeview(root, columns=cols, show="headings", height=5)

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=110, anchor="center")

data = [
    ("class0123", "Data design analysis", 3, "Session 2, Tuesday 20/09/2025 - 20/12/2025", "Not locked yet", "Cancel"),
    ("class0125", "Software technology", 3, "Session 3, Wednesday 21/09/2025 - 21/12/2025", "Not locked yet", "Cancel")
]

for row in data:
    tree.insert("", tk.END, values=row)

tree.pack(pady=10)

ttk.Label(root, text="Total tuition fee : xxxxxxx", font=("Arial", 12, "bold")).pack(pady=5)

root.mainloop()
