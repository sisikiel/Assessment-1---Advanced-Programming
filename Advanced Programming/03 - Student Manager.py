import tkinter as tk
from tkinter import ttk, messagebox #messagebox is for pop up message boxes, often used for alerting the user!
from tkinter import simpledialog #this helps the user to prompt an input using dialog boxes instead of entry widgets!


#file path for storing student data
FILE_PATH = "Advanced Programming/studentMarks.txt"

# Loading and saving data
def load_data():
    students = []  #Empty list to store the student records!

    try:
        #Open the data file in read mode
        with open(FILE_PATH, 'r') as f:
            #Read all lines from the file, strip whitespace, and ignore empty lines
            lines = [line.strip() for line in f.readlines() if line.strip()]

            #The first line is expected to contain the number of students (not strictly needed)
            n = int(lines[0])

            #Process each line after the first (each line = one student record)
            for line in lines[1:]:
                #Split CSV line into individual fields: id, name, coursework marks, exam mark
                sid, name, c1, c2, c3, exam = line.split(",")

                #Convert coursework and exam marks from string to integer
                c1, c2, c3, exam = map(int, (c1, c2, c3, exam))

                #Sum the coursework marks
                total_course = c1 + c2 + c3

                #Calculate overall marks including the exam
                overall = total_course + exam

                #Calculate percentage out of 160 total marks
                percent = (overall / 160) * 100

                #Determine grade based on percentage
                grade = (
                    "A" if percent >= 70 else
                    "B" if percent >= 60 else
                    "C" if percent >= 50 else
                    "D" if percent >= 40 else "F"
                )

                #Store all relevant information in a dictionary
                students.append({
                    "id": sid.strip(),
                    "name": name.strip(),
                    "coursework": total_course,
                    "exam": exam,
                    "overall": overall,
                    "percent": percent,
                    "grade": grade
                })

        #Print a message confirming the file loaded successfully
        print(f"Loaded '{FILE_PATH}' successfully.")
        return students  #Return the list of student dictionaries

    except FileNotFoundError:
        #If the file doesn't exist, show an error message to the user
        messagebox.showerror("Error", "File not found")
        return []  #Return an empty list in case of error


def save_data():
    # save students back to file
    with open(FILE_PATH, "w") as f:
        f.write(str(len(students)) + "\n")  #first line = student count
        for s in students:
            c_each = s['coursework'] // 3  #split coursework back into 3 parts
            f.write(f"{s['id']},{s['name']},{c_each},{c_each},{c_each},{s['exam']}\n")
            # each student on new line

# Display helpers section: 

def format_student(s):
    #make a nice formatted string for output box
    return "{:<35} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        s['name'], s['id'], s['coursework'], s['exam'],
        f"{s['percent']:.2f}%", s['grade']
    )

def show_header():
    #show column headers in text box
    output.insert(tk.END, "{:<35} {:<6} {:<12} {:<10} {:<10} {:<6}\n".format(
        "Name", "ID", "Coursework", "Exam", "Overall %", "Grade"
    ))
    output.insert(tk.END, "-" * 85 + "\n")  # separator line

def refresh_dropdown():
    #update combobox options with current student names
    student_dropdown["values"] = [s["name"] for s in students]


#The Main menu button actions section: 

def view_all():
    output.delete("1.0", tk.END)  #clear previous text
    if not students:
        output.insert(tk.END, "No student records available.")  #empty case
        return
    show_header()
    total_percent = 0
    for s in students:
        output.insert(tk.END, format_student(s))  #add student row
        total_percent += s["percent"]  #sum for average
    avg = total_percent / len(students)  #calculate average
    output.insert(tk.END, "\nTotal Students: {}\n".format(len(students)))
    output.insert(tk.END, "Average Percentage: {:.2f}%\n".format(avg))

def view_individual():
    output.delete("1.0", tk.END)
    sel = student_var.get()  #get selected student from combobox
    if not sel:
        output.insert(tk.END, "Please select a student.")  #no selection
        return
    for s in students:
        if s["name"] == sel:  # match by name
            show_header()
            output.insert(tk.END, format_student(s))
            return
    output.insert(tk.END, f"No record found for {sel}")  #not found

def show_highest():
    output.delete("1.0", tk.END)
    if not students: return
    best = max(students, key=lambda s: s["overall"])  #max overall marks
    output.insert(tk.END, "Highest Scorer:\n\n")
    show_header()
    output.insert(tk.END, format_student(best))

def show_lowest():
    output.delete("1.0", tk.END)
    if not students: return
    worst = min(students, key=lambda s: s["overall"])  #min overall marks
    output.insert(tk.END, "Lowest Scorer:\n\n")
    show_header()
    output.insert(tk.END, format_student(worst))

def sort_records():
    if not students:
        messagebox.showinfo("No Data", "No records to sort.")  # nothing to do
        return
    choice = messagebox.askquestion("Sort Order", "Sort ascending by name? (No = descending)")
    ascending = (choice == "yes")  #convert yes/no to boolean
    # sort list in place
    students.sort(key=lambda s: s["name"].lower(), reverse=not ascending)
    save_data()  #save sorted list
    refresh_dropdown()  #update combobox
    view_all()  #refresh text display
    messagebox.showinfo("Sorted", "Student records sorted successfully!")


#Adding new or deleting student records area: 

def manage_students_window():
    win = tk.Toplevel(root)  #new window
    win.title("Manage Students")
    win.geometry("400x300")
    win.configure(bg="#f0e5cf")
    win.resizable(False, False)
    tk.Label(win, text="Manage Student Records", font=("Times New Roman", 18, "bold"),
             bg="#d2b48c", fg="#3b2f2f", relief="ridge", bd=3, pady=5).pack(fill="x", pady=10)

    # ADDING STUDENT
    def add_student():
        #Create a new pop-up window for adding a student
        add_win = tk.Toplevel(win)
        add_win.title("Add Student")
        add_win.geometry("400x400")
        add_win.configure(bg="#f5deb3")
        add_win.resizable(False, False)  # prevent resizing

        #Add a heading label at the top of the window
        tk.Label(
            add_win, 
            text="Add New Student", 
            font=("Times New Roman", 16, "bold"),
            bg="#d2b48c", fg="#3b2f2f", relief="ridge", bd=3, pady=5
        ).pack(fill="x", pady=10)

        #Frame to hold the form inputs
        form_frame = tk.Frame(add_win, bg="#f5deb3")
        form_frame.pack(pady=10)

        #Labels for each input field
        labels = ["Student ID:", "Name:", "Coursework 1:", "Coursework 2:", "Coursework 3:", "Exam:"]
        entries = []  # to store the Entry widgets

        #Create input rows dynamically
        for i, lbl in enumerate(labels):
            row_frame = tk.Frame(form_frame, bg="#f5deb3")  # frame for each row
            row_frame.pack(pady=5, fill="x", padx=20)

            # Label on the left
            tk.Label(
                row_frame, text=lbl, bg="#f5deb3", font=("Times New Roman", 12, "bold"),
                width=15, anchor="e"  # right-aligned
            ).pack(side="left")

            # Entry box on the right
            e = tk.Entry(row_frame, width=20, font=("Times New Roman", 12))
            e.pack(side="left", padx=5)

            entries.append(e)  # store reference for later use

        #Function to handle submission of the new student
        def submit_add():
            try:
                # Get student ID and name from the first two entries
                sid, name = entries[0].get(), entries[1].get()

                # Get numeric marks for coursework and exam
                c1, c2, c3, exam = map(int, [
                    entries[2].get(), entries[3].get(), entries[4].get(), entries[5].get()
                ])
            except ValueError:
                # Show error if user enters non-numeric marks
                messagebox.showerror("Error", "Please enter valid numeric scores.")
                return

            #Calculate totals and percentages
            total_course = c1 + c2 + c3
            overall = total_course + exam
            percent = (overall / 160) * 100

            #Determine grade based on percentage
            grade = (
                "A" if percent >= 70 else
                "B" if percent >= 60 else
                "C" if percent >= 50 else
                "D" if percent >= 40 else
                "F"
            )

            #Add the student as a dictionary to the global students list
            students.append({
                "id": sid,
                "name": name,
                "coursework": total_course,
                "exam": exam,
                "overall": overall,
                "percent": percent,
                "grade": grade
            })

            #Save data to file after adding
            save_data()

            #Update UI elements
            refresh_dropdown()  # refresh combobox with new student
            view_all()          # refresh main display table

            #Inform user of successful addition
            messagebox.showinfo("Success", f"Student '{name}' added successfully.")

            #Close the add student window
            add_win.destroy()

        #Add a submit button that calls submit_add when clicked
        tk.Button(
            add_win,
            text="Add Student",
            bg="#8b4513",
            fg="white",
            font=("Times New Roman", 12, "bold"),
            relief="raised",
            bd=3,
            width=20,
            command=submit_add
        ).pack(pady=20)

        # DELETING STUDENT
    def delete_student():
        del_win = tk.Toplevel(win)  #new window
        del_win.title("Delete Student")
        del_win.geometry("350x200")
        del_win.configure(bg="#f5deb3")

        tk.Label(del_win, text="Enter Name or ID:", font=("Times New Roman", 12, "bold"),
                 bg="#f5deb3").pack(pady=15)
        entry = tk.Entry(del_win, width=25, font=("Times New Roman", 12))  # input box
        entry.pack(pady=5)

        def confirm_delete():
            name = entry.get().strip()  #get input and remove spaces
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
                del_win.destroy()  #close window

        tk.Button(del_win, text="Delete", bg="#a0522d", fg="white",
                  font=("Times New Roman", 12, "bold"), relief="raised",
                  bd=3, width=12, command=confirm_delete).pack(pady=20)

    #Buttons in Manage window 
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
        # Get input values from the update form
        name_id = entry_name.get().strip()  #Student ID or Name entered by user
        field = field_var.get().lower()     #Field to update (coursework, exam, name, or id)
        value = entry_value.get().strip()   #New value for the selected field

        #Basic validation: check that all fields are filled
        if not name_id or not field or not value:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        #Loop through all students to find the matching record
        for s in students:
            if s["name"].lower() == name_id.lower() or s["id"] == name_id:
                try:
                    #Determine which field to update and apply new value
                    if field == "coursework":
                        s["coursework"] = int(value)  #must be an integer
                    elif field == "exam":
                        s["exam"] = int(value)        #must be an integer
                    elif field == "name":
                        s["name"] = value             #updating name
                    elif field == "id":
                        s["id"] = value               #update ID
                    else:
                        messagebox.showerror("Error", "Invalid field selected.")
                        return
                except ValueError:
                    # Handle non-numeric input for coursework or exam
                    messagebox.showerror(
                        "Error", "Please enter a valid numeric value for coursework/exam."
                    )
                    return

                # Recalculate totals, percentage, and grade after update
                s["overall"] = s["coursework"] + s["exam"]
                s["percent"] = (s["overall"] / 160) * 100
                s["grade"] = (
                    "A" if s["percent"] >= 70 else
                    "B" if s["percent"] >= 60 else
                    "C" if s["percent"] >= 50 else
                    "D" if s["percent"] >= 40 else "F"
                )

                # Save changes to file and refresh UI
                save_data()           # save updated data
                refresh_dropdown()    # refresh combobox with updated student info
                view_all()            # refresh main display table

                # Notify user of successful update
                messagebox.showinfo(
                    "Updated", f"Record for {s['name']} updated successfully."
                )

                upd_win.destroy()  # Close the update window
                return  # Exit function after updating

        # If no student matches the input name/ID, inform the user
        messagebox.showinfo(
            "Not Found", f"No student found with name or ID '{name_id}'."
        )

    #Create the Update button and link it to submit_update()
    tk.Button(
        upd_win, text="Update Record", bg="#8b4513", fg="white",
        font=("Times New Roman", 12, "bold"), relief="raised", bd=3,
        width=20, command=submit_update
    ).pack(pady=20)

#The Main GUI setup ---

root = tk.Tk()
root.title("Student Manager")
root.geometry("950x700")
root.configure(bg="#f0e5cf")

#title label
title = tk.Label(root, text="Student Manager",
                 font=("Times New Roman", 22, "bold"),
                 bg="#d2b48c", fg="#3b2f2f", pady=10, padx=20,
                 relief="ridge", bd=4)
title.pack(pady=10)

#button frame
btn_frame = tk.Frame(root, bg="#f0e5cf")
btn_frame.pack(pady=10)

#common button style
button_style = {
    "font": ("Times New Roman", 13, "bold"),
    "relief": "raised", "bd": 3,
    "width": 22, "height": 2, "cursor": "hand2"
}

# main menu buttons settings
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
indiv_frame = tk.LabelFrame(
    root, 
    text="View Individual Record",     
    font=("Times New Roman", 14, "bold"),   
    bg="#f0e5cf", fg="#3b2f2f",                       
    bd=4, relief="groove", #Border style
    padx=10, pady=10                                   
)
indiv_frame.pack(pady=15) # Add some space below the frame

# Create a Tkinter StringVar to store the selected student from the dropdown
student_var = tk.StringVar()

# Combobox to allow user to select a student
student_dropdown = ttk.Combobox(
    indiv_frame, textvariable=student_var, # Link selection to student_var
    font=("Courier New", 12, "bold"),         
    width=25  # Width of dropdown section
)
student_dropdown.grid(row=0, column=0, padx=10, pady=5)

# Button to view the selected student's record
tk.Button(
    indiv_frame, 
    text="View Record",                       
    font=("Times New Roman", 12, "bold"),     
    bg="#a0522d", fg="white",         
    relief="raised", bd=3, width=18, height=1, 
    command=view_individual      # Function called when clicked
).grid(row=0, column=1, padx=10) # Place next to dropdown

# Output display setting

# Create a labeled frame to hold the output text box for student records
output_frame = tk.LabelFrame(
    root, 
    text="Student Records Display",                
    font=("Times New Roman", 14, "bold"),        
    bg="#f0e5cf", fg="#3b2f2f",             
    bd=4, relief="groove",            
    padx=10, pady=10                              
)
output_frame.pack(fill="both", expand=True, padx=15, pady=10)  # Fill space and add margins

# Text widget to display student records
output = tk.Text(
    output_frame, 
    height=20, width=100,                            
    font=("Courier New", 12, "bold"),                
    bg="#fff8dc", fg="#3b2f2f",  
    relief="sunken", bd=3                             
)
output.pack(fill="both", expand=True, pady=5) # Fill the frame and allow resizing

# Loading data and start GUI
students = load_data()  # load student data from file
refresh_dropdown()  # populate combobox
root.mainloop()  # start tkinter
