import tkinter as tk
import subprocess
import time
import sys
import os

# ---------- запуск камеры ----------
def start_program():
    loading_label.config(text="Loading... Please wait")
    root.update()

    python_path = sys.executable
    script_path = os.path.join(os.getcwd(), "main.py")

    subprocess.Popen(
        [python_path, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(4)
    root.withdraw()


# ---------- эффект нажатия кнопки ----------
def button_press(event):
    btn.config(font=("Helvetica", 19, "bold"))

def button_release(event):
    btn.config(font=("Helvetica", 18, "bold"))


# ---------- GUI ----------
root = tk.Tk()
root.title("Gesture Control")

root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg="#f7f8fa")

main_frame = tk.Frame(root, bg="#f7f8fa")
main_frame.pack(expand=True)

# Заголовок
label = tk.Label(
    main_frame,
    text="Система управления курсором",
    font=("Helvetica", 28, "bold"),
    bg="#f7f8fa",
    fg="#222222"
)
label.pack(pady=30)

# Описание
info = tk.Label(
    main_frame,
    text="Управляйте курсором с помощью руки",
    font=("Helvetica", 14),
    bg="#f7f8fa",
    fg="#555555"
)
info.pack(pady=10)

# ---------- кнопка Старт ----------
btn = tk.Button(
    main_frame,
    text="Старт",
    command=start_program,
    font=("Helvetica", 22),
    width=18,
    height=2,
    bg="#e6e6e6",
    fg="black",
    relief="flat",
    activebackground="#dcdcdc",
    activeforeground="black"
)

btn.pack(pady=50)


# ---------- эффект нажатия (уменьшение размера) ----------
def press_effect(event):
    btn.config(font=("Helvetica", 21))

def release_effect(event):
    btn.config(font=("Helvetica", 22))

btn.bind("<ButtonPress-1>", press_effect)
btn.bind("<ButtonRelease-1>", release_effect)


# ---------- загрузка ----------
loading_label = tk.Label(
    main_frame,
    text="",
    font=("Helvetica", 12),
    bg="#f7f8fa",
    fg="#888888"
)
loading_label.pack(pady=10)

# ---------- рамка инструкции ----------
instruction_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="solid",
    padx=30,
    pady=25
)

instruction_frame.pack(pady=(0, 150))

instruction_text = """ Инструкция пользователя

• Вытяните указательный палец — курсор двигается
• Сведите указательный и средний пальцы — клик мыши
• Вытяните все пальцы — прокрутка вверх
• Сожмите руку в кулак и отведите большой палец — прокрутка вниз
• Нажмите Esc для выхода из программы

⚠️ Держите руку в поле зрения камеры
"""

instruction_label = tk.Label(
    instruction_frame,
    text=instruction_text,
    font=("Helvetica", 18),
    justify="center",
    bg="white"
)

instruction_label.pack()

root.mainloop()