import cv2

# Open the webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame (optional: for mirror effect)
    frame = cv2.flip(frame, 1)

    # Show the frame
    cv2.imshow("Webcam Feed", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()