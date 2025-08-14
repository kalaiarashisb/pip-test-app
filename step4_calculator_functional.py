import cv2
import numpy as np
import math
import time

# ----------- Define Button Class -----------
class Button:
    def __init__(self, pos, text):
        self.pos = pos  # (x, y)
        self.text = text
        self.size = (60, 60)

    def draw(self, img, hover=False):
        x, y = self.pos
        color = (0, 255, 0) if hover else (255, 0, 0)
        cv2.rectangle(img, (x, y), (x + self.size[0], y + self.size[1]), color, -1)
        cv2.putText(img, self.text, (x + 15, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def is_hovered(self, x, y):
        bx, by = self.pos
        bw, bh = self.size
        return bx < x < bx + bw and by < y < by + bh

# ----------- Initialize Calculator Buttons -----------
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+']
]

buttons = []
for i in range(4):
    for j in range(4):
        pos = (70 + j * 70, 150 + i * 70)
        buttons.append(Button(pos, button_values[i][j]))

# ----------- Calculator Logic -----------
def evaluate_expression(expr):
    try:
        return str(eval(expr))
    except:
        return "Error"

# ----------- Main Program -----------
cap = cv2.VideoCapture(0)
detector = cv2.createBackgroundSubtractorMOG2()
expression = ""
last_click_time = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
    mask = detector.apply(imgBlur)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finger_x, finger_y = -1, -1

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 3000:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            (x, y, w, h) = cv2.boundingRect(approx)
            finger_x = x + w // 2
            finger_y = y + h // 2
            cv2.circle(img, (finger_x, finger_y), 10, (0, 255, 255), cv2.FILLED)

    # Draw all buttons
    for button in buttons:
        hovered = button.is_hovered(finger_x, finger_y)
        button.draw(img, hover=hovered)

    # Check button click
    if finger_x != -1 and finger_y != -1:
        for button in buttons:
            if button.is_hovered(finger_x, finger_y):
                current_time = time.time()
                if current_time - last_click_time > 1:
                    val = button.text
                    if val == 'C':
                        expression = ""
                    elif val == '=':
                        expression = evaluate_expression(expression)
                    else:
                        expression += val
                    last_click_time = current_time

    # Draw Expression Display
    cv2.rectangle(img, (70, 70), (350, 120), (255, 255, 255), -1)
    cv2.putText(img, expression, (80, 110), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 0), 2)

    cv2.imshow("Virtual Calculator", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
