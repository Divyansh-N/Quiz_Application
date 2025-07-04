import tkinter as tk
from tkinter import messagebox
import random

questions = [
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Processing Unit", "Central Print Unit", "Control Processing Unit"],
        "answer": "Central Processing Unit"
    },
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which language is used for web apps?",
        "options": ["Python", "HTML", "C++", "Java"],
        "answer": "HTML"
    },
    {
        "question": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "answer": "12"
    },
    {
        "question": "Who invented Python?",
        "options": ["Dennis Ritchie", "James Gosling", "Guido van Rossum", "Bjarne Stroustrup"],
        "answer": "Guido van Rossum"
    }
]

users = {}
current_user = ""
quiz_data = []
user_answers = []
timer_seconds = 15


def start_quiz():
    global quiz_data, user_answers
    quiz_data = random.sample(questions, 5)
    user_answers = [None] * len(quiz_data)
    show_question(0)


def show_question(index):
    def next_question():
        selected = var.get()
        if selected != "":
            user_answers[index] = selected
        else:
            user_answers[index] = None
        timer_label.after_cancel(timer)
        if index + 1 < len(quiz_data):
            show_question(index + 1)
        else:
            show_results()

    def update_timer(time_left):
        nonlocal timer
        timer_label.config(text=f"Time left: {time_left}s")
        if time_left > 0:
            timer = timer_label.after(1000, update_timer, time_left - 1)
        else:
            user_answers[index] = var.get() if var.get() != "" else None
            if index + 1 < len(quiz_data):
                show_question(index + 1)
            else:
                show_results()

    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#fffaf0")

    q = quiz_data[index]
    question_label = tk.Label(root, text=f"Q{index+1}: {q['question']}", font=("Helvetica", 16, "bold"), bg="#fffaf0", wraplength=700, justify="left")
    question_label.pack(pady=30)

    var = tk.StringVar(value="")

    for opt in q['options']:
        tk.Radiobutton(root, text=opt, variable=var, value=opt, font=("Helvetica", 14), bg="#fffaf0").pack(anchor="w", padx=100)

    global timer_label
    timer_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red", bg="#fffaf0")
    timer_label.pack(pady=10)

    tk.Button(root, text="Next", command=next_question, font=("Helvetica", 14), bg="#4169e1", fg="white", width=15).pack(pady=20)

    timer = None
    update_timer(timer_seconds)


def show_results():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="#f5f5f5")

    score = sum(
        1 for i in range(len(quiz_data))
        if user_answers[i] == quiz_data[i]['answer']
    )

    tk.Label(root, text=f"Quiz Completed, {current_user}!", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=10)
    tk.Label(root, text=f"Your Score: {score}/{len(quiz_data)}", font=("Helvetica", 16), bg="#f5f5f5").pack(pady=10)
    tk.Label(root, text="Review:", font=("Helvetica", 14, "underline"), bg="#f5f5f5").pack(pady=10)

    for i, q in enumerate(quiz_data):
        frame = tk.Frame(root, bg="#f5f5f5")
        frame.pack(pady=5, anchor="w", padx=20)

        tk.Label(frame, text=f"Q{i+1}: {q['question']}", font=("Helvetica", 12, "bold"), bg="#f5f5f5", wraplength=700).pack(anchor="w")
        ua = user_answers[i]
        ca = q['answer']
        ua_text = f"Your answer: {ua if ua else 'No answer'}"
        ca_text = f"Correct answer: {ca}"
        color = "green" if ua == ca else "red"

        tk.Label(frame, text=ua_text, fg=color, font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w")
        tk.Label(frame, text=ca_text, fg="blue", font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="w")

    tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 14), bg="#dc143c", fg="white", width=10).pack(pady=20)



def login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x400")
    root.config(bg="#f0f8ff")

    tk.Label(root, text="Welcome to Smart Quiz", font=("Helvetica", 20, "bold"), bg="#f0f8ff").pack(pady=20)

    tk.Label(root, text="Username:", font=("Helvetica", 14), bg="#f0f8ff").pack()
    username_entry = tk.Entry(root, font=("Helvetica", 14))
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:", font=("Helvetica", 14), bg="#f0f8ff").pack()
    password_entry = tk.Entry(root, font=("Helvetica", 14), show="*")
    password_entry.pack(pady=5)

    def login():
        global current_user
        uname = username_entry.get()
        passwd = password_entry.get()
        if uname in users and users[uname] == passwd:
            current_user = uname
            start_quiz()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def signup():
        uname = username_entry.get()
        passwd = password_entry.get()
        if uname in users:
            messagebox.showerror("Error", "Username already exists")
        elif not uname or not passwd:
            messagebox.showerror("Error", "Fields cannot be empty")
        else:
            users[uname] = passwd
            messagebox.showinfo("Success", "User registered successfully")

    tk.Button(root, text="Login", command=login, font=("Helvetica", 14), bg="#4169e1", fg="white", width=15).pack(pady=10)
    tk.Button(root, text="Signup", command=signup, font=("Helvetica", 14), bg="#32cd32", fg="white", width=15).pack()


root = tk.Tk()
root.title("Python Quiz App")
root.geometry("800x600")
login_screen()
root.mainloop()
