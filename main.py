import cv2
import autopy
import mediapipe as mp
import math
import numpy as np
import pyautogui
import tkinter as tk
import time
import sys


# эффект нажатия
def press_effect(event):
    btn.config(font=("Helvetica", 21))


def release_effect(event):
    btn.config(font=("Helvetica", 22))


# запуск камеры
def start_program():
    loading_label.config(text="Loading...")
    root.update()
    root.withdraw()
    main_proc()


def cl(result):  # проверка, сведены ли пальцы
    x8 = result.multi_hand_landmarks[0].landmark[8].x
    y8 = result.multi_hand_landmarks[0].landmark[8].y
    x12 = result.multi_hand_landmarks[0].landmark[12].x
    y12 = result.multi_hand_landmarks[0].landmark[12].y
    s128 = math.hypot(x8 - x12, y8 - y12)
    if s128 < 0.02:
        return True


def scroll_down_check(result):  # проверка, что все пальцы согнуты, кроме большого
    hand = result.multi_hand_landmarks[0]
    y4 = hand.landmark[4].y
    y2 = hand.landmark[2].y
    if abs(y2 - y4) < 0.05:
        if not finger2(result) and not finger3(result) and not finger4(result):
            return True


def finger2(results):  # проверка, выпрямлен ли второй палец
    a5x = results.multi_hand_landmarks[0].landmark[5].x
    a5y = results.multi_hand_landmarks[0].landmark[5].y
    a6x = results.multi_hand_landmarks[0].landmark[6].x
    a6y = results.multi_hand_landmarks[0].landmark[6].y
    a7x = results.multi_hand_landmarks[0].landmark[7].x
    a7y = results.multi_hand_landmarks[0].landmark[7].y
    a8x = results.multi_hand_landmarks[0].landmark[8].x
    a8y = results.multi_hand_landmarks[0].landmark[8].y
    a0x = results.multi_hand_landmarks[0].landmark[0].x
    a0y = results.multi_hand_landmarks[0].landmark[0].y
    if math.hypot(a5x - a0x, a5y - a0y) < math.hypot(a6x - a0x, a6y - a0y) < math.hypot(a7x - a0x,
                                                                                        a7y - a0y) < math.hypot(
        a8x - a0x, a8y - a0y):
        return True


def finger3(results):  # проверка, выпрямлен ли третий палец
    a5x = results.multi_hand_landmarks[0].landmark[13].x
    a5y = results.multi_hand_landmarks[0].landmark[13].y
    a6x = results.multi_hand_landmarks[0].landmark[14].x
    a6y = results.multi_hand_landmarks[0].landmark[14].y
    a7x = results.multi_hand_landmarks[0].landmark[15].x
    a7y = results.multi_hand_landmarks[0].landmark[15].y
    a8x = results.multi_hand_landmarks[0].landmark[16].x
    a8y = results.multi_hand_landmarks[0].landmark[16].y
    a0x = results.multi_hand_landmarks[0].landmark[0].x
    a0y = results.multi_hand_landmarks[0].landmark[0].y
    if math.hypot(a5x - a0x, a5y - a0y) < math.hypot(a6x - a0x, a6y - a0y) < math.hypot(a7x - a0x,
                                                                                        a7y - a0y) < math.hypot(
        a8x - a0x, a8y - a0y):
        return True


def finger4(results):  # проверка, выпрямлен ли четвертый палец
    a5x = results.multi_hand_landmarks[0].landmark[17].x
    a5y = results.multi_hand_landmarks[0].landmark[17].y
    a6x = results.multi_hand_landmarks[0].landmark[18].x
    a6y = results.multi_hand_landmarks[0].landmark[18].y
    a7x = results.multi_hand_landmarks[0].landmark[19].x
    a7y = results.multi_hand_landmarks[0].landmark[19].y
    a8x = results.multi_hand_landmarks[0].landmark[20].x
    a8y = results.multi_hand_landmarks[0].landmark[20].y
    a0x = results.multi_hand_landmarks[0].landmark[0].x
    a0y = results.multi_hand_landmarks[0].landmark[0].y
    if math.hypot(a5x - a0x, a5y - a0y) < math.hypot(a6x - a0x, a6y - a0y
                                            ) < math.hypot(a7x - a0x, a7y - a0y) < math.hypot(a8x - a0x, a8y - a0y):
        return True


def main_proc():
    cap = cv2.VideoCapture(0)
    width, height = autopy.screen.size()
    pyautogui.PAUSE = 0

    # начальная позиция курсора
    prev_x = width / 2
    prev_y = height / 2

    SMOOTHING = 0.7
    SENSITIVITY = 2.2

    # обнаружние руки
    hands = mp.solutions.hands.Hands(static_image_mode=False,
                                     max_num_hands=1,
                                     min_tracking_confidence=0.3,
                                     min_detection_confidence=0.3)

    mpDraw = mp.solutions.drawing_utils  # создание объекта для дальнейшего рисования линий на руке

    last_click = 0
    cv2.namedWindow("Handtrack", cv2.WINDOW_NORMAL)

    while True:
        _, img = cap.read()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)  # обнаружение точек на руке

        if result and result.multi_hand_landmarks:  # проверка, что рука на экране
            f2 = finger2(result)
            f3 = finger3(result)
            f4 = finger4(result)
            sd = scroll_down_check(result)
            click_check = cl(result)
            hand = result.multi_hand_landmarks[0]
            lm = hand.landmark[8]

            h, w, _ = img.shape
            cx = int(lm.x * w)
            cy = int(lm.y * h)

            cv2.circle(img, (cx, cy), 3, (355, 0, 255))

            if result and result.multi_hand_landmarks and f2:  # проверка, выпрямлен ли второй палец и есть ли 8 точка
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                center_x = w / 2
                center_y = h / 2

                dx = cx - center_x
                dy = cy - center_y

                x_screen = width / 2 - dx * SENSITIVITY
                y_screen = height / 2 + dy * SENSITIVITY

                # ограничения на координаты, чтобы не выйти за экран
                margin = 5
                x_screen = max(margin, min(width - margin, x_screen))
                y_screen = max(margin, min(height - margin, y_screen))

                # сглаживание движения
                x_screen = prev_x + (x_screen - prev_x) * SMOOTHING
                y_screen = prev_y + (y_screen - prev_y) * SMOOTHING

                prev_x = x_screen
                prev_y = y_screen

                # движение курсора
                autopy.mouse.move(x_screen, y_screen)

                current_time = time.time()

                if f2 and f3 and f4:  # прокрутка вверх
                    pyautogui.scroll(1)

                elif click_check and f2 and current_time - last_click > 0.4:  # защита от двойного клика
                    autopy.mouse.click()
                    last_click = current_time

            elif sd:  # прокрутка вниз
                    pyautogui.scroll(-1)

            # рисование линий между точками на руке
            mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0],
                                  mp.solutions.hands.HAND_CONNECTIONS)

        img = np.fliplr(img)

        cv2.imshow('Handtrack', img)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()

    cap.release()
    cv2.destroyAllWindows()


# GUI
root = tk.Tk()
root.title("Gesture Control")

root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg="#f7f8fa")

main_frame = tk.Frame(root, bg="#f7f8fa")  # создание контейнера
main_frame.pack(expand=True)

# заголовок
label = tk.Label(
    main_frame,
    text="Система управления курсором",
    font=("Helvetica", 28, "bold"),
    bg="#f7f8fa",
    fg="#222222"
)
label.pack(pady=30)

# описание
info = tk.Label(
    main_frame,
    text="Управляйте курсором с помощью руки",
    font=("Helvetica", 14),
    bg="#f7f8fa",
    fg="#555555"
)
info.pack(pady=10)

# кнопка "старт"
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
btn.bind("<ButtonPress-1>", press_effect)
btn.bind("<ButtonRelease-1>", release_effect)


# режим загрузки
loading_label = tk.Label(
    main_frame,
    text="",
    font=("Helvetica", 12),
    bg="#f7f8fa",
    fg="#888888"
)
loading_label.pack(pady=10)

# инструкция
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