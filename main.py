import cv2
import autopy
import mediapipe as mp
import math
import numpy as np
import pyautogui

# проверка пальцев
def cl(result):  # проверка, сведены ли пальцы
    x8 = result.multi_hand_landmarks[0].landmark[8].x
    y8 = result.multi_hand_landmarks[0].landmark[8].y
    x12 = result.multi_hand_landmarks[0].landmark[12].x
    y12 = result.multi_hand_landmarks[0].landmark[12].y
    s128 = math.hypot(x8 - x12, y8 - y12)
    if s128 < 0.05:
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

# обнаружние руки
hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=1,
                                 min_tracking_confidence=0.3,
                                 min_detection_confidence=0.3)

mpDraw = mp.solutions.drawing_utils  # создание объекта для дальнейшего рисования линий на руке
while True:  # осоновной цикл программы
    _, img = cap.read()  # считывае изображения с камеры
    result = hands.process(img)  # обнаружение точек на руке
    if result.multi_hand_landmarks:  # проверка, рука и точки на экране
        for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):  # перебор всех точек на руке
            h, w, _ = img.shape  # получение размеров изображения
            cx, cy = int(lm.x * w), int(lm.y * h)  # координаты рассматриваемой точки

            cv2.circle(img, (cx, cy), 3, (355, 0, 255))  # рисование кружка на точке

            if finger2(result) and id == 8:  # проверка на то, выпрямлен ли второй палец и есть ли 8 точка (подушечка второго пальца)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                if cx > 15 and cx < width - 180 and cy > 0 and cy < height:  # проверка координат пальца на то, находится ли она в рамках экрана
                    autopy.mouse.move((width - (cx * width) / w), (cy * height) / (h))  # передвижение мышки на указанные координаты




                if finger2(result) and finger3(result) and finger4(result):  # прокрутка вверх — все пальцы выпрямлены
                    pyautogui.scroll(3)

                elif cl(result) and finger2(result):  # обнаружение жеста для клика
                    autopy.mouse.click()  # клик


            elif scroll_down_check(result):  # прокрутка вниз — кулак
                    pyautogui.scroll(-3)

        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)  # рисование линий между точками на руке

    img = np.fliplr(img)  # отзеркаливание изображения, чтобы курсор двигался в нужную сторону
    cv2.imshow('Handtrack', img)  # показ изображения
    cv2.waitKey(1)  # команда, которая позволяет окну с изображением не закрываться
