import tkinter as tk
import subprocess
import time
import sys
import os

def close_app(event):
    root.destroy()  # Закрыть окно

def start_program():
    loading_label.config(text="Loading... Please wait")
    root.update()

    python_path = sys.executable
    script_path = os.path.join(os.getcwd(), "main.py")

    # запускаем камеру
    process = subprocess.Popen(
        [python_path, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # ждём, пока камера процесс начнёт работать
    time.sleep(4)

    # скрываем стартовое окно только после запуска
    root.withdraw()


root = tk.Tk()
root.title("Gesture Control")
root.geometry("600x400")

root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.state('zoomed')
loading_label = tk.Label(root, text="")
loading_label.pack()

# Заголовок
label = tk.Label(root,
                 text="Gesture Control System",
                 font=("Arial", 18))
label.pack(pady=30)

# Описание (очень коротко — можно для защиты)
info = tk.Label(root,
                text="Start program to activate camera gesture control",
                font=("Arial", 11))
info.pack(pady=10)

# Кнопка запуска
btn = tk.Button(root,
                text="Start",
                width=20,
                height=2,
                command=start_program)
btn.pack(pady=40)

instruction_text = """
📌 Инструкция пользователя

• Вытяните указательный палец — курсор двигается.
• Сведите указательный и средний пальцы — клик мыши.
• Вытяните все пальцы — прокрутка вверх.
• Сожмите руку в кулак и отведите большой палец — прокрутка вниз.
• Нажмите Esc для выхода из программы.

⚠️ Держите руку в поле зрения камеры.
"""

instruction_label = tk.Label(
    root,
    text=instruction_text,
    font=("Arial", 11),
    justify="left"
)

instruction_label.pack(pady=20)


root.mainloop()

