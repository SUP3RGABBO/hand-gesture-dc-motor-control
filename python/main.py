import cv2 as cv
import mediapipe as mp
import serial
import time
import math


last_speed = -1


arduino = serial.Serial(port='COM4', baudrate=9600, timeout=0.1)
time.sleep(2)


cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)


min_distance = 0.011
max_distance = 0.433

def get_color(pwm_val):
    """Colore sfumatura: rosso → giallo → verde"""
    ratio = pwm_val / 255
    if ratio < 0.5:
        r = 255
        g = int(255 * (ratio * 2))
    else:
        r = int(255 * (1 - (ratio - 0.5) * 2))
        g = 255
    b = 0
    return (b, g, r)


def draw_text_with_outline(img, text, pos, font, scale, color, thickness):
    """Disegna testo bianco con contorno nero"""
    x, y = pos

    cv.putText(img, text, (x-1, y-1), font, scale, (0,0,0), thickness+2)
    cv.putText(img, text, (x+1, y-1), font, scale, (0,0,0), thickness+2)
    cv.putText(img, text, (x-1, y+1), font, scale, (0,0,0), thickness+2)
    cv.putText(img, text, (x+1, y+1), font, scale, (0,0,0), thickness+2)

    cv.putText(img, text, (x, y), font, scale, color, thickness)

while True:
    success, frame = cap.read()
    if not success:
        continue

    RGB_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        thumbTip = hand_landmarks.landmark[4]
        indexTip = hand_landmarks.landmark[8]


        distance = math.sqrt((thumbTip.x - indexTip.x)**2 + (thumbTip.y - indexTip.y)**2)


        pwm_val = int((distance - min_distance) / (max_distance - min_distance) * 255)
        pwm_val = max(0, min(pwm_val, 255))


        if abs(pwm_val - last_speed) > 2:
            arduino.write(f"{pwm_val}\n".encode())
            last_speed = pwm_val


        bar_x1, bar_x2 = 50, 80
        bar_y_bottom = frame.shape[0]
        bar_height = int((pwm_val / 255) * (frame.shape[0]-50))
        bar_y_top = bar_y_bottom - bar_height


        cv.rectangle(frame, (bar_x1-2, bar_y_bottom), (bar_x2+2, bar_y_bottom-(frame.shape[0]-50)), (0,0,0), 2)


        color = get_color(pwm_val)
        for i in range(bar_height):
            ratio = i / bar_height
            r = int(color[2] * ratio + 0 * (1-ratio))
            g = int(color[1] * ratio + 0 * (1-ratio))
            b = int(color[0] * ratio + 0 * (1-ratio))
            cv.line(frame, (bar_x1, bar_y_bottom-i), (bar_x2, bar_y_bottom-i), (b,g,r), 1)


        draw_text_with_outline(frame, f"Speed: {pwm_val}", (bar_x2+10, bar_y_top+10),
                               cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv.imshow("Hand Tracking Motor Control", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
