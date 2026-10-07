import cv2

# Initialize webcam (0 is usually the built-in camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera. Please check permissions or camera switch.")
else:
    print("Webcam connected! Press 'q' on the video window to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the webcam feed
    cv2.imshow("Webcam Test Stream", frame)

    # Press 'q' to close
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()