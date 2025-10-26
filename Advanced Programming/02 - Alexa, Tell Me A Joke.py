import tkinter as tk
import random

#Loading the joke file
def load_jokes_from_file(filename):
    jokes_list = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|") #the jokes are split by using |. 
                if len(parts) == 2:
                    jokes_list.append((parts[0], parts[1])) #parts [0] are the jokes, while parts [1] are the punchlines.
    except FileNotFoundError:
        print("Jokes file not found.")
    return jokes_list

jokes = load_jokes_from_file("Advanced Programming/jokes.txt")

current_joke = None

#The main inputs
def handle_input():
    global current_joke
    
    #this ensures that the submitted input will work even if the letters aren't capitalized properly
    user_input = input_entry.get().strip().lower() 
    if user_input == "alexa tell me a joke":
        current_joke = random.choice(jokes) #random joke generator = their matching punchline 
        joke_label.config(text=current_joke[0])
        
        main_button.config(text="Show Punchline", command=show_punchline) #button to show punchline
    else:
        joke_label.config(text="Please type exactly: Alexa tell me a Joke") #when user types different input.

def show_punchline():
    setup, punchline = current_joke
    joke_label.config(text=f"{setup}\n\n{punchline}") #\n\n is used for spacing to give cleaner look. 
    main_button.config(text="Submit", command=handle_input)
    input_entry.delete(0, tk.END)

#GUI settings
root = tk.Tk()
root.title("Pink Joke Teller")
root.geometry("700x500")
root.config(bg="#ffc0cb")

#title heading
title_label = tk.Label(root, text="Type 'Alexa tell me a Joke' below:",
                       font=("Garamond", 20, "bold"), bg="#ffc0cb")
title_label.pack(pady=(40, 20))

#user input (where they have to enter the phrase "Alexa tell me a joke")
input_entry = tk.Entry(root, font=("Garamond", 16), width=30, justify="center")
input_entry.pack(pady=10)

#the joke label settings when the submit button is pressed
joke_label = tk.Label(root, text="", font=("Garamond", 18, "bold"),
                      bg="#ffc0cb", wraplength=600, justify="center")
joke_label.pack(expand=True)

bottom_frame = tk.Frame(root, bg="#ffc0cb")
bottom_frame.pack(side="bottom", pady=40)

#main button - submitting
main_button = tk.Button(bottom_frame, text="Submit", font=("Garamond", 16, "bold"),
                        bg="#ff69b4", width=20, height=2, command=handle_input)
main_button.grid(row=0, column=0, padx=10)

#quit button
quit_button = tk.Button(bottom_frame, text="Quit", font=("Garamond", 16, "bold"),
                        bg="#ff1493", width=15, height=2, command=root.quit)
quit_button.grid(row=0, column=1, padx=10)

#loading and running the data:
root.mainloop()
