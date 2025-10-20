import tkinter as tk
from tkinter import ttk, messagebox

def load_data():
    students = []
    try:
        with open('Advanced Programming/studentMarks.txt', 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            n = int(lines[0])
            for line in lines[1:]:
                sid, name, c1, c2, c3, exam = line.split(",")
                c1, c2, c3, exam = map(int, (c1, c2, c3, exam))
                total_course = c1 + c2 + c3
                overall = total_course + exam
                percent = (overall / 160) * 100
                grade = (
                    "A" if percent >= 70 else
                    "B" if percent >= 60 else
                    "C" if percent >= 50 else
                    "D" if percent >= 40 else "F"
                )
                students.append({
                    "id": sid,
                    "name": name,
                    "coursework": total_course,
                    "exam": exam,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })
        print("✅ File 'Advanced Programming/studentMarks.txt' opened successfully.")
        return students
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return []

# 🌟 Format students in columns with fixed widths
def format_student(s):
    return "{:<20} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        s['name'], s['id'], s['coursework'], s['exam'],
        f"{s['percent']:.2f}%", s['grade']
    )

def view_all():
    output.delete("1.0", tk.END)
    if not students: return
    # Header
    output.insert(tk.END, "{:<20} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-"*70 + "\n")
    total_percent = 0
    for s in students:
        output.insert(tk.END, format_student(s))
        total_percent += s["percent"]
    avg = total_percent / len(students)
    output.insert(tk.END, "\nTotal Students: {}\n".format(len(students)))
    output.insert(tk.END, "Average Percentage: {:.2f}%\n".format(avg))

def view_individual():
    output.delete("1.0", tk.END)
    sel = student_var.get()
    if not sel: return
    output.insert(tk.END, "{:<20} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-"*70 + "\n")
    for s in students:
        if s["name"] == sel:
            output.insert(tk.END, format_student(s))
            break

def show_highest():
    output.delete("1.0", tk.END)
    if not students: return
    best = max(students, key=lambda s: s["overall"])
    output.insert(tk.END, "Highest Scorer:\n\n")
    output.insert(tk.END, "{:<20} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-"*70 + "\n")
    output.insert(tk.END, format_student(best))

def show_lowest():
    output.delete("1.0", tk.END)
    if not students: return
    worst = min(students, key=lambda s: s["overall"])
    output.insert(tk.END, "Lowest Scorer:\n\n")
    output.insert(tk.END, "{:<20} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-"*70 + "\n")
    output.insert(tk.END, format_student(worst))

# Main Window
root = tk.Tk()
root.title("Student Manager")
root.geometry("800x600")
root.configure(bg="#f0e5cf")  # warm beige

title = tk.Label(root, text="Student Manager",
                 font=("Times New Roman", 22, "bold"),
                 bg="#d2b48c", fg="#3b2f2f", pady=10, padx=20,
                 relief="ridge", bd=4)
title.pack(pady=15)

# Button Frame
btn_frame = tk.Frame(root, bg="#f0e5cf")
btn_frame.pack(pady=10)

button_style = {
    "font": ("Times New Roman", 13, "bold"),
    "relief": "raised",
    "bd": 3,
    "width": 22,
    "height": 2,
    "cursor": "hand2"
}

tk.Button(btn_frame, text="View All Student Records",
          bg="#f5deb3", fg="#3b2f2f", command=view_all, **button_style).grid(row=0, column=0, padx=8)
tk.Button(btn_frame, text="Show Highest Score",
          bg="#deb887", fg="#3b2f2f", command=show_highest, **button_style).grid(row=0, column=1, padx=8)
tk.Button(btn_frame, text="Show Lowest Score",
          bg="#cd853f", fg="white", command=show_lowest, **button_style).grid(row=0, column=2, padx=8)

# Individual Record
indiv_frame = tk.LabelFrame(root, text="View Individual Record",
                            font=("Times New Roman", 14, "bold"),
                            bg="#f0e5cf", fg="#3b2f2f", bd=4, relief="groove",
                            padx=10, pady=10)
indiv_frame.pack(pady=20)

student_var = tk.StringVar()
student_dropdown = ttk.Combobox(indiv_frame, textvariable=student_var,
                                font=("Courier New", 12, "bold"), width=25)
student_dropdown.grid(row=0, column=0, padx=10, pady=5)

tk.Button(indiv_frame, text="View Record",
          font=("Times New Roman", 12, "bold"),
          bg="#8b4513", fg="white", relief="raised",
          bd=3, width=18, height=1, command=view_individual).grid(row=0, column=1, padx=10)

# Output Box with Monospace Font
output_frame = tk.LabelFrame(root, text="Student Records Display",
                             font=("Times New Roman", 14, "bold"),
                             bg="#f0e5cf", fg="#3b2f2f", bd=4, relief="groove",
                             padx=10, pady=10)
output_frame.pack(pady=10)

output = tk.Text(output_frame, height=20, width=90,
                 font=("Courier New", 12, "bold"), bg="#fff8dc", fg="#3b2f2f",
                 relief="sunken", bd=3)
output.pack(pady=5)

scrollbar = tk.Scrollbar(output_frame, command=output.yview)
scrollbar.pack(side="right", fill="y")
output.config(yscrollcommand=scrollbar.set)

# Load Data
students = load_data()
student_dropdown["values"] = [s["name"] for s in students]

root.mainloop()
