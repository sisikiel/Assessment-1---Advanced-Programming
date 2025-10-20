import tkinter as tk
import random

def load_jokes_from_file(filename):
    jokes_list = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # Split setup and punchline by "|"
                parts = line.strip().split("|")
                if len(parts) == 2:
                    jokes_list.append((parts[0], parts[1]))
    except FileNotFoundError:
        print("Jokes file not found.")
    return jokes_list

jokes = load_jokes_from_file("Advanced Programming/jokes.txt")

class JokeApp:
    def __init__(self, root):
        
        # main window setup
        self.root = root
        self.root.title("Pink Joke Teller")
        self.root.geometry("700x500")
        self.root.config(bg="#ffc0cb")
        
        # title label
        self.title_label = tk.Label(root, text="Type 'Alexa tell me a Joke' below:",
                                    font=("Garamond", 20, "bold"), bg="#ffc0cb")
        
        self.title_label.pack(pady=(40, 20))  # (top padding, bottom padding)
        
        # user input field
        self.input_entry = tk.Entry(root, font=("Garamond", 16), width=30, justify="center")
        self.input_entry.pack(pady=10)
        
        # joke text display area
        self.joke_label = tk.Label(root, text="", font=("Garamond", 18, "bold"),
                                   bg="#ffc0cb", wraplength=600, justify="center")
        self.joke_label.pack(expand=True)
        
        # bottom frame for buttons
        bottom_frame = tk.Frame(root, bg="#ffc0cb")
        bottom_frame.pack(side="bottom", pady=40)
        
        # submit button
        self.main_button = tk.Button(bottom_frame, text="Submit",
                                     font=("Garamond", 16, "bold"), bg="#ff69b4",
                                     width=20, height=2, command=self.handle_input)
        self.main_button.grid(row=0, column=0, padx=10)
        
        # quit button
        self.quit_button = tk.Button(bottom_frame, text="Quit",
                                     font=("Garamond", 16, "bold"), bg="#ff1493",
                                     width=15, height=2, command=root.quit)
        self.quit_button.grid(row=0, column=1, padx=10)
        
        # state tracking variables
        self.current_joke = None
        self.showing_punchline = False
        
        
    def handle_input(self):
        # get user input and normalize text
        user_input = self.input_entry.get().strip().lower()

        # check if input matches the trigger phrase
        if user_input == "alexa tell me a joke":
            self.current_joke = random.choice(jokes)
            self.joke_label.config(text=self.current_joke[0])  # show setup
            self.main_button.config(text="Show Punchline", command=self.show_punchline)
        else:
            self.joke_label.config(text="Please type exactly: Alexa tell me a Joke")


    def show_punchline(self):
        # display punchline of the current joke
        setup, punchline = self.current_joke
        self.joke_label.config(text=f"{setup}\n\n{punchline}")
        self.main_button.config(text="Submit", command=self.handle_input)
        self.input_entry.delete(0, tk.END)  # clear input

root = tk.Tk()
app = JokeApp(root)
root.mainloop()