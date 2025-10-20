import tkinter as tk
from tkinter import ttk
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("600x400")
        self.root.configure(bg="#001f3f")

        # variables
        self.score = 0
        self.question_num = 0
        self.level = None
        self.num1 = 0
        self.num2 = 0
        self.operation = ''
        self.message_label = None

        # simple button style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        font=("Times New Roman", 14, "bold"),
                        foreground="white",
                        background="#3a3a90",
                        padding=10)
        style.map("TButton", background=[("active", "#5a5ac0")])

        self.displayMenu()

    def clear_window(self):
        # clear all widgets from screen
        for widget in self.root.winfo_children():
            widget.destroy()

    # function to display menu
    def displayMenu(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#001f3f")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Welcome to Math Quiz",
                 font=("Times New Roman", 24, "bold"),
                 fg="white", bg="#001f3f").pack(pady=10)

        tk.Label(frame, text="Select Difficulty Level",
                 font=("Times New Roman", 18),
                 fg="white", bg="#001f3f").pack(pady=10)

        ttk.Button(frame, text="Easy", command=lambda: self.start_quiz(1)).pack(pady=8)
        ttk.Button(frame, text="Moderate", command=lambda: self.start_quiz(2)).pack(pady=8)
        ttk.Button(frame, text="Advanced", command=lambda: self.start_quiz(3)).pack(pady=8)

    # function to generate random number
    def randomInt(self, level):
        if level == 1:
            return random.randint(1, 9)
        elif level == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    # function to decide + or -
    def decideOperation(self):
        return random.choice(['+', '-'])

    # function to display the math problem
    def displayProblem(self, q_num, num1, num2, operation):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#001f3f")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=f"Question {q_num}/10",
                 font=("Times New Roman", 16),
                 fg="white", bg="#001f3f").pack(pady=5)

        tk.Label(frame, text=f"{num1} {operation} {num2} = ?",
                 font=("Times New Roman", 22, "bold"),
                 fg="white", bg="#001f3f").pack(pady=10)

        self.answer_entry = tk.Entry(frame, font=("Times New Roman", 16),
                                     bg="#1e1e3f", fg="white",
                                     insertbackground="white", justify="center")
        self.answer_entry.pack(pady=5)
        self.answer_entry.focus()

        ttk.Button(frame, text="Submit", command=self.check_answer).pack(pady=10)

        # label for showing result messages
        self.message_label = tk.Label(frame, text="",
                                      font=("Times New Roman", 14),
                                      fg="white", bg="#001f3f")
        self.message_label.pack(pady=10)

    # function to check if answer is correct
    def isCorrect(self, user_answer, correct_answer, attempt):
        if user_answer == correct_answer:
            points = 10 if attempt == 1 else 5
            self.score += points
            self.message_label.config(text=f"Correct! +{points} points", fg="#00ff7f")
            return True
        else:
            if attempt == 1:
                self.message_label.config(text="Incorrect, try again!", fg="#ff6666")
                return False
            else:
                self.message_label.config(text=f"Wrong again! The answer was {correct_answer}.", fg="#ff6666")
                return True

    # function to show final score
    def displayResults(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#001f3f")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Quiz Complete!",
                 font=("Times New Roman", 20, "bold"),
                 fg="white", bg="#001f3f").pack(pady=10)

        tk.Label(frame, text=f"Your Score: {self.score}/100",
                 font=("Times New Roman", 16),
                 fg="white", bg="#001f3f").pack(pady=10)

        # assign grade
        if self.score >= 90:
            grade = "A+"
        elif self.score >= 80:
            grade = "A"
        elif self.score >= 70:
            grade = "B"
        elif self.score >= 60:
            grade = "C"
        elif self.score >= 50:
            grade = "D"
        else:
            grade = "F"

        tk.Label(frame, text=f"Grade: {grade}",
                 font=("Times New Roman", 16, "bold"),
                 fg="white", bg="#001f3f").pack(pady=5)

        ttk.Button(frame, text="Play Again", command=self.displayMenu).pack(pady=10)
        ttk.Button(frame, text="Exit", command=self.root.quit).pack(pady=5)

    # start quiz
    def start_quiz(self, level):
        self.level = level
        self.score = 0
        self.question_num = 0
        self.next_question()

    # go to next question
    def next_question(self):
        if self.question_num >= 10:
            self.displayResults()
            return

        self.num1 = self.randomInt(self.level)
        self.num2 = self.randomInt(self.level)
        self.operation = self.decideOperation()
        self.attempt = 1
        self.question_num += 1
        self.displayProblem(self.question_num, self.num1, self.num2, self.operation)

    # check answer and give feedback
    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.message_label.config(text="Please enter a valid number.", fg="#ff6666")
            return

        correct_answer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2
        result = self.isCorrect(user_answer, correct_answer, self.attempt)

        if result:
            # delay next question slightly to show message
            self.root.after(1000, self.next_question)
        else:
            self.attempt += 1
            self.answer_entry.delete(0, tk.END)

# run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()
