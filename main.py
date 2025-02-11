import os
import sys
from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 1
time = None

# Function to get the correct path for the image when running as an EXE
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(time)
    canvas.itemconfig(timer, text="00:00")
    label.config(text="TIMER")
    check_label.config(text="")
    global reps
    reps = 1

# ---------------------------- TIMER MECHANISM ------------------------------- # 

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def start_timer():
    global reps
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps % 2 == 1:
        count_down(work_sec)
        label.config(text="WORK", fg=RED)
    elif reps % 8 == 0:
        count_down(long_break_sec)
        label.config(text="LONG BREAK", fg=PINK)
    else:
        count_down(short_break_sec)
        label.config(text="BREAK", fg=GREEN)
    reps += 1

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_sec == 0:
        count_sec = "00"

    canvas.itemconfig(timer, text=f"{count_min}:{count_sec}")
    if count > 0:
        global time
        time = window.after(1000, count_down, count-1)
    else:
        start_timer()
        marks = " "
        work_session = math.floor(reps/2)
        for _ in range(work_session):
            marks += "✔"
        check_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodora")
window.config(padx=100, pady=50, bg=YELLOW)

label = Label(text="TIMER", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 45))
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
check_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME))

# Use resource_path to correctly load the image
tomato_img = PhotoImage(file=resource_path("tomato.png"))
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

label.grid(column=1, row=0)
canvas.grid(column=1, row=1)
start_button.grid(column=0, row=2)
reset_button.grid(column=2, row=2)
check_label.grid(column=1, row=3)

window.mainloop()
