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
        if theme == 'dark':
            button_color = (50, 50, 50)
            text_color = (255, 255, 255)
        else:
            button_color = (200, 200, 200)
            text_color = (0, 0, 0)
        cv2.rectangle(img, (x, y), (x + self.size[0], y + self.size[1]), button_color, -1)
        cv2.rectangle(img, (x, y), (x + self.size[0], y + self.size[1]), (100, 100, 100), 2)
        cv2.putText(img, self.text, (x + 15, y + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    def is_clicked(self, x, y):
        bx, by = self.pos
        bw, bh = self.size
        return bx < x < bx + bw and by < y < by + bh

# Button layout
button_values = [['7', '8', '9', '/'],
                 ['4', '5', '6', '*'],
                 ['1', '2', '3', '-'],
                 ['C', '0', '=', '+']]

# Create all button instances
buttons = []
for i in range(4):
    for j in range(4):
        pos = (70 + j * 70, 150 + i * 70)
        buttons.append(Button(pos, button_values[i][j]))

# Calculator logic
equation = ''
theme = 'light'

# Mouse callback
def click_event(event, x, y, flags, param):
    global equation, theme
    if event == cv2.EVENT_LBUTTONDOWN:
        for button in buttons:
            if button.is_clicked(x, y):
                value = button.text
                if value == 'C':
                    equation = ''
                elif value == '=':
                    try:
                        equation = str(eval(equation))
                    except:
                        equation = 'Error'
                else:
                    equation += value
        # Toggle theme if top-left corner clicked
        if x < 50 and y < 50:
            theme = 'dark' if theme == 'light' else 'light'

# Create OpenCV window
cv2.namedWindow("Calculator")
cv2.setMouseCallback("Calculator", click_event)

while True:
    # Create blank canvas
    img = np.zeros((500, 400, 3), np.uint8)
    
    if theme == 'dark':
        img[:] = (30, 30, 30)
        text_color = (255, 255, 255)
    else:
        img[:] = (255, 255, 255)
        text_color = (0, 0, 0)

    # Draw display
    cv2.rectangle(img, (50, 50), (350, 100), (200, 200, 200), -1)
    cv2.putText(img, equation, (60, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw buttons
    for button in buttons:
        button.draw(img, theme)

    # Theme toggle corner
    cv2.rectangle(img, (10, 10), (40, 40), (100, 100, 255), -1)
    cv2.putText(img, "T", (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show image
    cv2.imshow("Calculator", img)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
