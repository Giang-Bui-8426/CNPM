import tkinter as tk
from tkinter import ttk, messagebox

def edit_profile():
    for entry in entries.values():
        entry.config(state="normal")

def save_profile():
    for entry in entries.values():
        entry.config(state="readonly")
    messagebox.showinfo("Save", "Profile saved successfully!")

def cancel_edit():
    for entry in entries.values():
        entry.config(state="readonly")

root = tk.Tk()
root.title("Student Profile")
root.geometry("500x350")
root.config(bg="#D9D9D9")

frame = tk.Frame(root, bg="#D9D9D9")
frame.pack(pady=20)

ttk.Label(frame, text="Student Profile", font=("Arial", 18, "bold"), background="#D9D9D9").grid(row=0, column=0, columnspan=2, pady=10)

labels = ["Student ID", "Full Name", "Email", "Major", "Class", "Phone"]
values = ["21123456", "Nguyễn Văn A", "nguyenvana@uth.edu.vn", "Smart Logistics", "D21CLC01", "0901 234 567"]

entries = {}
for i, (label, value) in enumerate(zip(labels, values)):
    ttk.Label(frame, text=f"{label} :").grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
    entry = ttk.Entry(frame, width=30)
    entry.insert(0, value)
    entry.config(state="readonly")
    entry.grid(row=i+1, column=1, padx=5, pady=5)
    entries[label] = entry

btn_frame = tk.Frame(root, bg="#D9D9D9")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Edit", width=10, bg="#90EE90", command=edit_profile).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Save", width=10, bg="#32CD32", command=save_profile).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Cancel", width=10, bg="#FF6347", command=cancel_edit).grid(row=0, column=2, padx=5)

root.mainloop()
