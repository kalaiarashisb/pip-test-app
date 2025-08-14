import cv2
import numpy as np

# Define the Button class
class Button:
    def __init__(self, pos, text):
        self.pos = pos  # (x, y)
        self.text = text
        self.size = (60, 60)

    def draw(self, img, theme='light'):
        x, y = self.pos
        w, h = self.size

        if theme == 'dark':
            button_color = (50, 50, 50)
            text_color = (255, 255, 255)
        else:
            button_color = (200, 200, 200)
            text_color = (0, 0, 0)

        # Draw button
        cv2.rectangle(img, (x, y), (x + w, y + h), button_color, cv2.FILLED)
        # Draw border
        cv2.rectangle(img, (x, y), (x + w, y + h), (100, 100, 100), 2)
        # Draw text
        font_scale = 1.2
        thickness = 2
        (text_w, text_h), _ = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_PLAIN, font_scale, thickness)
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, text_color, thickness)

    def is_clicked(self, x, y):
        btn_x, btn_y = self.pos
        w, h = self.size
        return btn_x < x < btn_x + w and btn_y < y < btn_y + h


# Define calculator layout
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', 'C', '=', '+']
]

buttons = []
for i in range(4):
    for j in range(4):
        pos = (70 + j * 70, 100 + i * 70)
        buttons.append(Button(pos, button_values[i][j]))

# Variables
equation = ""

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)  # Flip to mirror user

    # Draw the equation/output area
    cv2.rectangle(img, (70, 30), (350, 80), (255, 255, 255), -1)
    cv2.putText(img, equation, (80, 65), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # Draw buttons
    for button in buttons:
        button.draw(img)

    # Simulate gesture with mouse click (for now)
    def click_event(event, x, y, flags, param):
        global equation
        if event == cv2.EVENT_LBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(x, y):
                    val = button.text
                    if val == "C":
                        equation = ""
                    elif val == "=":
                        try:
                            equation = str(eval(equation))
                        except:
                            equation = "Error"
                    else:
                        equation += val

    cv2.setMouseCallback("Gesture Calculator", click_event)

    cv2.imshow("Gesture Calculator", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
