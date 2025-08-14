import cv2
import mediapipe as mp
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Define calculator button layout
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['C', '0', '=', '+']
]

# ---------- Button Class ----------
class Button:
    def __init__(self, pos, text):
        self.pos = pos        # (x, y) position
        self.text = text
        self.size = (60, 60)  # width, height

    def draw(self, img, hover=False):
        x, y = self.pos
        color = (0, 255, 0) if hover else (255, 0, 0)  # Green if hovering
        cv2.rectangle(img, (x, y), (x + self.size[0], y + self.size[1]), color, -1)
        cv2.putText(img, self.text, (x + 15, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def is_hovered(self, x, y):
        bx, by = self.pos
        bw, bh = self.size
        return bx < x < bx + bw and by < y < by + bh

# ---------- Create Buttons ----------
buttons = []
start_x, start_y = 50, 100
for i in range(4):
    for j in range(4):
        btn_pos = (start_x + j * 70, start_y + i * 70)
        btn_text = button_values[i][j]
        buttons.append(Button(btn_pos, btn_text))

# ---------- Main Loop ----------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingertip = None

    # Hand detection
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            # Get index fingertip (landmark 8)
            x = int(handLms.landmark[8].x * w)
            y = int(handLms.landmark[8].y * h)
            fingertip = (x, y)

            # Draw fingertip circle
            cv2.circle(frame, fingertip, 10, (0, 255, 255), cv2.FILLED)

    # Draw calculator buttons and check hover
    for button in buttons:
        if fingertip and button.is_hovered(*fingertip):
            button.draw(frame, hover=True)
        else:
            button.draw(frame)

    cv2.imshow("Virtual Calculator UI", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
