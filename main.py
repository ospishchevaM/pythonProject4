import cv2
import autopy
import mediapipe as mp
import math
import numpy as np
import pyautogui
import time



# проверка пальцев
def cl(result):  # проверка, сведены ли пальцы
    x8 = result.multi_hand_landmarks[0].landmark[8].x
    y8 = result.multi_hand_landmarks[0].landmark[8].y
    x12 = result.multi_hand_landmarks[0].landmark[12].x
    y12 = result.multi_hand_landmarks[0].landmark[12].y
    s128 = math.hypot(x8 - x12, y8 - y12)
    if s128 < 0.04:
        return True

def scroll_down_check(result):  # проверка, что все пальцы согнуты, кроме большого
    hand = result.multi_hand_landmarks[0]
    y4 = hand.landmark[4].y
    y2 = hand.landmark[2].y
    if abs(y2 - y4) < 0.05:
        if not finger2(result) and not finger3(result) and not finger4(result):
            return True


def finger2(results):  # проверка выпрямлен ли второй палец
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


def finger3(results):  # проверка выпрямлен ли третий палец
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


def finger4(results):  # проверка выпрямлен ли четвертый палец
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
    if math.hypot(a5x - a0x, a5y - a0y) < math.hypot(a6x - a0x, a6y - a0y) < math.hypot(a7x - a0x,
                                                                                        a7y - a0y) < math.hypot(
        a8x - a0x, a8y - a0y):
        return True


cap = cv2.VideoCapture(0)  # получение изображения с камеры
width, height = autopy.screen.size()  # получение размеров экрана
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

last_click = 0  # время последнего клика

while True:
    _, img = cap.read()  # считывание изображения с камеры

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)  # обнаружение точек на руке

    if result and result.multi_hand_landmarks:  # проверка, рука и точки на экране
        f2 = finger2(result)
        f3 = finger3(result)
        f4 = finger4(result)
        sd = scroll_down_check(result)
        click_check = cl(result)
        hand = result.multi_hand_landmarks[0]
        lm = hand.landmark[8]

        h, w, _ = img.shape  # получение размеров изображения
        cx = int(lm.x * w)
        cy = int(lm.y * h)

        cv2.circle(img, (cx, cy), 3, (355, 0, 255))  # рисование кружка на точке

        if f2:  # проверка на то, выпрямлен ли второй палец и есть ли 8 точка (подушечка второго пальца)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # рассчет центра экрана
            center_x = w / 2
            center_y = h / 2

            # насколько палец смещен от центра
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

            current_time = time.time()  # для клика

            if f2 and f3 and f4:  # прокрутка вверх — все пальцы выпрямлены
                pyautogui.scroll(3)


            elif click_check and f2 and current_time - last_click > 0.4:  # защита от двойного срабатывания
                    autopy.mouse.click()
                    last_click = current_time


        elif sd:  # прокрутка вниз — кулак с отставленным большим пальцем
                    pyautogui.scroll(-3)

        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)  # рисование линий между точками на руке

    img = np.fliplr(img)  # отзеркаливание изображения, чтобы курсор двигался в нужную сторону
    cv2.imshow('Handtrack', img)  # показ изображения
    cv2.waitKey(5)  # команда, которая позволяет окну с изображением не закрываться
