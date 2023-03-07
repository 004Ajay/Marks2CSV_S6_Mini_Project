import cv2
import os

# Create the folder if it doesn't exist
if not os.path.exists("captured_images"):
    os.mkdir("captured_images")

# Initialize the camera
cap = cv2.VideoCapture(0)

counter = 0

# Loop to continuously read frames from the camera
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Save the frame
    cv2.imwrite("captured_images/frame"+str(counter)+".jpg", frame)
    counter += 1

    # Display the frame
    cv2.imshow("Camera Feed", frame)

    # Check for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()

# Close all windows
cv2.destroyAllWindows()