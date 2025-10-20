import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

# file path for storing student data
FILE_PATH = "Advanced Programming/studentMarks.txt"

# Loading and saving data
def load_data():
    students = []
    try:
        with open(FILE_PATH, 'r') as f:
            # read all lines and remove empty ones
            lines = [line.strip() for line in f.readlines() if line.strip()]
            n = int(lines[0])  # first line = number of students (not really needed tho)
            for line in lines[1:]:
                sid, name, c1, c2, c3, exam = line.split(",")  # split CSV
                c1, c2, c3, exam = map(int, (c1, c2, c3, exam))  # convert to int
                total_course = c1 + c2 + c3  # sum coursework
                overall = total_course + exam  # total marks
                percent = (overall / 160) * 100  # calculate percentage
                # simple grading system
                grade = (
                    "A" if percent >= 70 else
                    "B" if percent >= 60 else
                    "C" if percent >= 50 else
                    "D" if percent >= 40 else "F"
                )
                # store everything in a dict
                students.append({
                    "id": sid.strip(),
                    "name": name.strip(),
                    "coursework": total_course,
                    "exam": exam,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })
        print(f"Loaded '{FILE_PATH}' successfully.")  # debugging print
        return students
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")  # show error to user
        return []

def save_data():
    # save students back to file
    with open(FILE_PATH, "w") as f:
        f.write(str(len(students)) + "\n")  # first line = student count
        for s in students:
            c_each = s['coursework'] // 3  # split coursework back into 3 parts
            f.write(f"{s['id']},{s['name']},{c_each},{c_each},{c_each},{s['exam']}\n")
            # each student on new line

# Display helpers section: 

def format_student(s):
    # make a nice formatted string for output box
    return "{:<35} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        s['name'], s['id'], s['coursework'], s['exam'],
        f"{s['percent']:.2f}%", s['grade']
    )

def show_header():
    # show column headers in text box
    output.insert(tk.END, "{:<35} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-" * 85 + "\n")  # separator line

def refresh_dropdown():
    # update combobox options with current student names
    student_dropdown["values"] = [s["name"] for s in students]


# The Main menu button actions section: 

def view_all():
    output.delete("1.0", tk.END)  # clear previous text
    if not students:
        output.insert(tk.END, "No student records available.")  # empty case
        return
    show_header()
    total_percent = 0
    for s in students:
        output.insert(tk.END, format_student(s))  # add student row
        total_percent += s["percent"]  # sum for average
    avg = total_percent / len(students)  # calculate average
    output.insert(tk.END, "\nTotal Students: {}\n".format(len(students)))
    output.insert(tk.END, "Average Percentage: {:.2f}%\n".format(avg))

def view_individual():
    output.delete("1.0", tk.END)
    sel = student_var.get()  # get selected student from combobox
    if not sel:
        output.insert(tk.END, "Please select a student.")  # no selection
        return
    for s in students:
        if s["name"] == sel:  # match by name
            show_header()
            output.insert(tk.END, format_student(s))
            return
    output.insert(tk.END, f"No record found for {sel}")  # not found

def show_highest():
    output.delete("1.0", tk.END)
    if not students: return
    best = max(students, key=lambda s: s["overall"])  # max overall marks
    output.insert(tk.END, "Highest Scorer:\n\n")
    show_header()
    output.insert(tk.END, format_student(best))

def show_lowest():
    output.delete("1.0", tk.END)
    if not students: return
    worst = min(students, key=lambda s: s["overall"])  # min overall marks
    output.insert(tk.END, "Lowest Scorer:\n\n")
    show_header()
    output.insert(tk.END, format_student(worst))

def sort_records():
    if not students:
        messagebox.showinfo("No Data", "No records to sort.")  # nothing to do
        return
    choice = messagebox.askquestion("Sort Order", "Sort ascending by name? (No = descending)")
    ascending = (choice == "yes")  # convert yes/no to boolean
    # sort list in place
    students.sort(key=lambda s: s["name"].lower(), reverse=not ascending)
    save_data()  # save sorted list
    refresh_dropdown()  # update combobox
    view_all()  # refresh text display
    messagebox.showinfo("Sorted", "Student records sorted successfully!")


# Adding new or deleting student records area: 

def manage_students_window():
    win = tk.Toplevel(root)  # new window
    win.title("Manage Students")
    win.geometry("400x300")
    win.configure(bg="#f0e5cf")
    win.resizable(False, False)
    tk.Label(win, text="Manage Student Records", font=("Times New Roman", 18, "bold"),
             bg="#d2b48c", fg="#3b2f2f", relief="ridge", bd=3, pady=5).pack(fill="x", pady=10)

    # ADDING STUDENT
    def add_student():
        add_win = tk.Toplevel(win)
        add_win.title("Add Student")
        add_win.geometry("400x400")
        add_win.configure(bg="#f5deb3")
        add_win.resizable(False, False)

        tk.Label(add_win, text="Add New Student", font=("Times New Roman", 16, "bold"),
                bg="#d2b48c", fg="#3b2f2f", relief="ridge", bd=3, pady=5).pack(fill="x", pady=10)

        form_frame = tk.Frame(add_win, bg="#f5deb3")
        form_frame.pack(pady=10)

        labels = ["Student ID:", "Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"]
        entries = []

        # create input rows dynamically
        for i, lbl in enumerate(labels):
            row_frame = tk.Frame(form_frame, bg="#f5deb3")
            row_frame.pack(pady=5, fill="x", padx=20)
            tk.Label(row_frame, text=lbl, bg="#f5deb3", font=("Times New Roman", 12, "bold"),
                     width=15, anchor="e").pack(side="left")
            e = tk.Entry(row_frame, width=20, font=("Times New Roman", 12))
            e.pack(side="left", padx=5)
            entries.append(e)

        def submit_add():
            try:
                sid, name = entries[0].get(), entries[1].get()
                c1, c2, c3, exam = map(int, [entries[2].get(), entries[3].get(), entries[4].get(), entries[5].get()])
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric scores.")  # invalid input
                return
            total_course = c1 + c2 + c3
            overall = total_course + exam
            percent = (overall / 160) * 100
            grade = ("A" if percent >= 70 else "B" if percent >= 60 else "C" if percent >= 50 else "D" if percent >= 40 else "F")
            # add to list
            students.append({
                "id": sid, "name": name, "coursework": total_course,
                "exam": exam, "overall": overall, "percent": percent, "grade": grade
            })
            save_data()  # save after add
            refresh_dropdown()  # update combobox
            view_all()  # refresh main display
            messagebox.showinfo("Success", f"Student '{name}' added successfully.")
            add_win.destroy()  # close window

        tk.Button(add_win, text="Add Student", bg="#8b4513", fg="white",
                font=("Times New Roman", 12, "bold"), relief="raised", bd=3, width=20,
                command=submit_add).pack(pady=20)


        # DELETING STUDENT
    def delete_student():
        del_win = tk.Toplevel(win)  # new window
        del_win.title("Delete Student")
        del_win.geometry("350x200")
        del_win.configure(bg="#f5deb3")

        tk.Label(del_win, text="Enter Name or ID:", font=("Times New Roman", 12, "bold"),
                 bg="#f5deb3").pack(pady=15)
        entry = tk.Entry(del_win, width=25, font=("Times New Roman", 12))  # input box
        entry.pack(pady=5)

        def confirm_delete():
            name = entry.get().strip()  # get input and remove spaces
            before = len(students)
            # remove any student that matches name or ID
            students[:] = [s for s in students if s["name"].lower() != name.lower() and s["id"] != name]
            if len(students) == before:
                messagebox.showinfo("Not Found", "No matching record found.")  # nothing removed
            else:
                save_data()  # save updated list
                refresh_dropdown()  # update combobox
                view_all()  # refresh main display
                messagebox.showinfo("Deleted", f"Record for '{name}' deleted successfully.")
                del_win.destroy()  # close window

        tk.Button(del_win, text="Delete", bg="#a0522d", fg="white",
                  font=("Times New Roman", 12, "bold"), relief="raised",
                  bd=3, width=12, command=confirm_delete).pack(pady=20)

    # ---- Buttons in Manage window ----
    tk.Button(win, text="Add Student", font=("Times New Roman", 13, "bold"),
              bg="#deb887", fg="#3b2f2f", relief="raised", bd=3, width=20,
              command=add_student).pack(pady=15)

    tk.Button(win, text="Delete Student", font=("Times New Roman", 13, "bold"),
              bg="#cd853f", fg="white", relief="raised", bd=3, width=20,
              command=delete_student).pack(pady=10)


# Updating the student record section:

def update_student():
    #Main window
    upd_win = tk.Toplevel(root)
    upd_win.title("Update Student Record")
    upd_win.geometry("400x400")
    upd_win.configure(bg="#f0e5cf")
    upd_win.resizable(False, False)

    tk.Label(upd_win, text="Update Student Record", font=("Times New Roman", 16, "bold"),
             bg="#d2b48c", fg="#3b2f2f", relief="ridge", bd=3, pady=5).pack(fill="x", pady=10)

    # form frame for input fields
    form_frame = tk.Frame(upd_win, bg="#f0e5cf")
    form_frame.pack(pady=10, padx=20)

    # student name/ID input
    tk.Label(form_frame, text="Enter Student Name or ID:", font=("Times New Roman", 12, "bold"),
             bg="#f0e5cf").grid(row=0, column=0, sticky="e", pady=5)
    entry_name = tk.Entry(form_frame, width=25, font=("Times New Roman", 12))
    entry_name.grid(row=0, column=1, pady=5, padx=5)

    # dropdown to select which field to update
    tk.Label(form_frame, text="Field to Update:", font=("Times New Roman", 12, "bold"),
             bg="#f0e5cf").grid(row=1, column=0, sticky="e", pady=5)
    field_var = tk.StringVar()
    field_dropdown = ttk.Combobox(form_frame, textvariable=field_var, font=("Times New Roman", 12),
                                  values=["coursework", "exam", "name", "id"], state="readonly", width=22)
    field_dropdown.grid(row=1, column=1, pady=5, padx=5)

    # input for new value
    tk.Label(form_frame, text="New Value:", font=("Times New Roman", 12, "bold"),
             bg="#f0e5cf").grid(row=2, column=0, sticky="e", pady=5)
    entry_value = tk.Entry(form_frame, width=25, font=("Times New Roman", 12))
    entry_value.grid(row=2, column=1, pady=5, padx=5)

    def submit_update():
        # get values from form
        name_id = entry_name.get().strip()
        field = field_var.get().lower()
        value = entry_value.get().strip()
        if not name_id or not field or not value:
            messagebox.showerror("Error", "Please fill all fields.")  # basic validation
            return

        # loop through students to find match
        for s in students:
            if s["name"].lower() == name_id.lower() or s["id"] == name_id:
                try:
                    # check which field to update
                    if field == "coursework":
                        s["coursework"] = int(value)
                    elif field == "exam":
                        s["exam"] = int(value)
                    elif field == "name":
                        s["name"] = value
                    elif field == "id":
                        s["id"] = value
                    else:
                        messagebox.showerror("Error", "Invalid field selected.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid numeric value for coursework/exam.")
                    return

                # recalc overall, percent and grade
                s["overall"] = s["coursework"] + s["exam"]
                s["percent"] = (s["overall"] / 160) * 100
                s["grade"] = (
                    "A" if s["percent"] >= 70 else
                    "B" if s["percent"] >= 60 else
                    "C" if s["percent"] >= 50 else
                    "D" if s["percent"] >= 40 else "F"
                )

                save_data()  # save changes
                refresh_dropdown()  # update dropdown
                view_all()  # refresh main display
                messagebox.showinfo("Updated", f"Record for {s['name']} updated successfully.")
                upd_win.destroy()  # close window
                return

        messagebox.showinfo("Not Found", f"No student found with name or ID '{name_id}'.")

    # update button
    tk.Button(upd_win, text="Update Record", bg="#8b4513", fg="white",
              font=("Times New Roman", 12, "bold"), relief="raised", bd=3,
              width=20, command=submit_update).pack(pady=20)


# The Main GUI setup

root = tk.Tk()
root.title("Student Manager")
root.geometry("950x700")
root.configure(bg="#f0e5cf")

# title label
title = tk.Label(root, text="Student Manager",
                 font=("Times New Roman", 22, "bold"),
                 bg="#d2b48c", fg="#3b2f2f", pady=10, padx=20,
                 relief="ridge", bd=4)
title.pack(pady=10)

# button frame
btn_frame = tk.Frame(root, bg="#f0e5cf")
btn_frame.pack(pady=10)

# common button style
button_style = {
    "font": ("Times New Roman", 13, "bold"),
    "relief": "raised", "bd": 3,
    "width": 22, "height": 2, "cursor": "hand2"
}

# main menu buttons
tk.Button(btn_frame, text="View All Student Records",
          bg="#f5deb3", fg="#3b2f2f", command=view_all, **button_style).grid(row=0, column=0, padx=6)
tk.Button(btn_frame, text="Show Highest Score",
          bg="#deb887", fg="#3b2f2f", command=show_highest, **button_style).grid(row=0, column=1, padx=6)
tk.Button(btn_frame, text="Show Lowest Score",
          bg="#cd853f", fg="white", command=show_lowest, **button_style).grid(row=0, column=2, padx=6)
tk.Button(btn_frame, text="Sort Student Records",
          bg="#e0c097", fg="#3b2f2f", command=sort_records, **button_style).grid(row=1, column=0, padx=6, pady=8)
tk.Button(btn_frame, text="Manage Students (Add/Delete)",
          bg="#b8860b", fg="white", command=manage_students_window, **button_style).grid(row=1, column=1, padx=6, pady=8)
tk.Button(btn_frame, text="Update Student Record",
          bg="#8b4513", fg="white", command=update_student, **button_style).grid(row=1, column=2, padx=6, pady=8)


# Viewing individual record frame section

indiv_frame = tk.LabelFrame(root, text="View Individual Record",
                            font=("Times New Roman", 14, "bold"),
                            bg="#f0e5cf", fg="#3b2f2f", bd=4, relief="groove",
                            padx=10, pady=10)
indiv_frame.pack(pady=15)

student_var = tk.StringVar()
student_dropdown = ttk.Combobox(indiv_frame, textvariable=student_var,
                                font=("Courier New", 12, "bold"), width=25)
student_dropdown.grid(row=0, column=0, padx=10, pady=5)

# view individual record button
tk.Button(indiv_frame, text="View Record",
          font=("Times New Roman", 12, "bold"),
          bg="#a0522d", fg="white", relief="raised",
          bd=3, width=18, height=1, command=view_individual).grid(row=0, column=1, padx=10)


# The output box section:

output_frame = tk.LabelFrame(root, text="Student Records Display",
                             font=("Times New Roman", 14, "bold"),
                             bg="#f0e5cf", fg="#3b2f2f", bd=4, relief="groove",
                             padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=15, pady=10)

output = tk.Text(output_frame, height=20, width=100,
                 font=("Courier New", 12, "bold"),
                 bg="#fff8dc", fg="#3b2f2f",
                 relief="sunken", bd=3)
output.pack(fill="both", expand=True, pady=5)

# add scrollbar
scrollbar = tk.Scrollbar(output_frame, command=output.yview)
scrollbar.pack(side="right", fill="y")
output.config(yscrollcommand=scrollbar.set)


# Loading data and start GUI

students = load_data()  # load student data from file
refresh_dropdown()  # populate combobox
root.mainloop()  # start tkinter
