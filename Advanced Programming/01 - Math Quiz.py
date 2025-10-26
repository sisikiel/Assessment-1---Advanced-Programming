import tkinter as tk
from tkinter import ttk
import random

#The global state (the variables that are accessible to be used anywhere within the code)
score = 0
question_num = 0
level = 1
num1 = 0
num2 = 0
operation = ''
attempt = 1
answer_entry = None
message_label = None

#Some helper functions:
def clear_window():
    #removes all widgets from the main window
    for widget in root.winfo_children():
        widget.destroy()

def randomInt(lvl):
    #returning random numbers depending on the difficulty chosen: 
    if lvl == 1:
        return random.randint(1, 9) #one digit numbers
    elif lvl == 2:
        return random.randint(10, 99) #two digit numbers
    else:
        return random.randint(1000, 9999) #four digit numbers

def decideOperation():
    #randomly chooses the arithmetic operator
    return random.choice(['+', '-'])

#Menu Display
def displayMenu():
    clear_window()
    frame = tk.Frame(root, bg="#001f3f") #main frame
    frame.place(relx=0.5, rely=0.5, anchor="center") #frame alignment 

    #frame label settings
    tk.Label(frame, text="Welcome to Math Quiz",
             font=("Times New Roman", 24, "bold"),
             fg="white", bg="#001f3f").pack(pady=10)

    tk.Label(frame, text="Select Difficulty Level",
             font=("Times New Roman", 18),
             fg="white", bg="#001f3f").pack(pady=10)

    #buttons - for level options!
    ttk.Button(frame, text="Easy", command=lambda: start_quiz(1)).pack(pady=8)
    ttk.Button(frame, text="Moderate", command=lambda: start_quiz(2)).pack(pady=8)
    ttk.Button(frame, text="Advanced", command=lambda: start_quiz(3)).pack(pady=8)

#Quiz Settings
def displayProblem(q_num, n1, n2, op): 
    global answer_entry, message_label
    clear_window()
    frame = tk.Frame(root, bg="#001f3f") #main frame
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text=f"Question {q_num}/10",
             font=("Times New Roman", 16),
             fg="white", bg="#001f3f").pack(pady=5)

    tk.Label(frame, text=f"{n1} {op} {n2} = ?",
             font=("Times New Roman", 22, "bold"),
             fg="white", bg="#001f3f").pack(pady=10)

    #entry frame for entering the user's answer
    answer_entry = tk.Entry(frame, font=("Times New Roman", 16),
                            bg="#1e1e3f", fg="white",
                            insertbackground="white", justify="center")
    answer_entry.pack(pady=5)
    answer_entry.focus()

    #check answer button
    ttk.Button(frame, text="Submit", command=check_answer).pack(pady=10)

    message_label = tk.Label(frame, text="",
                             font=("Times New Roman", 14),
                             fg="white", bg="#001f3f")
    message_label.pack(pady=10)

#checking if the answer is correct: 
def isCorrect(user_answer, correct_answer):
    global score, attempt, message_label
    if user_answer == correct_answer:
        points = 10 if attempt == 1 else 5 #first attempt, the user gets +10 points! 2nd attempt lets users get +5 points
        score += points #adding the score
        
        message_label.config(text=f"Correct! +{points} points", fg="#00ff7f") #displaying the score
        return True
    else:
        if attempt == 1: #when the answer is incorrect after two tries
            message_label.config(text="Incorrect, try again!", fg="#ff6666")
            return False
        else:
            message_label.config(text=f"Wrong again! The answer was {correct_answer}.", fg="#ff6666") #shows the correct answer
            return True

#displaying the result after the quiz
def displayResults():
    clear_window()
    frame = tk.Frame(root, bg="#001f3f") #main frame
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Quiz Complete!",
             font=("Times New Roman", 20, "bold"),
             fg="white", bg="#001f3f").pack(pady=10)

    tk.Label(frame, text=f"Your Score: {score}/100",
             font=("Times New Roman", 16),
             fg="white", bg="#001f3f").pack(pady=10)

    # assigning the grade depending on the user's score:
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    #displaying the final grade
    tk.Label(frame, text=f"Grade: {grade}",
             font=("Times New Roman", 16, "bold"),
             fg="white", bg="#001f3f").pack(pady=5)

    ttk.Button(frame, text="Play Again", command=displayMenu).pack(pady=10) #asks users if they want to play again
    ttk.Button(frame, text="Exit", command=root.quit).pack(pady=5)


# The main quiz flow:
def start_quiz(lvl):
    #variables to store and keep in track the user's answers
    global level, score, question_num
    level = lvl
    score = 0
    question_num = 0
    next_question()

def next_question():
    global num1, num2, operation, attempt, question_num
    if question_num >= 10:
        displayResults()
        return
    num1 = randomInt(level) #asssigns random number depending on the chosen level
    num2 = randomInt(level)
    operation = decideOperation()
    attempt = 1
    question_num += 1
    displayProblem(question_num, num1, num2, operation) #displays the problem


def check_answer():
    global attempt
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        message_label.config(text="Please enter a valid number.", fg="#ff6666") #if user doesn't input anything/integer.=
        return

    correct_answer = num1 + num2 if operation == '+' else num1 - num2 #for checking the correct answer
    result = isCorrect(user_answer, correct_answer)

    if result:
        root.after(1000, next_question)
    else:
        attempt += 1
        answer_entry.delete(0, tk.END)
        
        
#Main settings
root = tk.Tk()
root.title("Math Quiz")
root.geometry("600x400")
root.configure(bg="#001f3f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton",
                font=("Times New Roman", 14, "bold"),
                foreground="white",
                background="#3a3a90",
                padding=10)
style.map("TButton", background=[("active", "#5a5ac0")])

displayMenu()
root.mainloop()
