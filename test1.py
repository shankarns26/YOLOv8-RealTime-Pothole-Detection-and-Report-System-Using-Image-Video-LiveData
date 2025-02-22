from ultralytics import YOLO
import cv2

# Load the YOLO model
model = YOLO(r"C:\Users\admin\Downloads\best (4).pt")  # Ensure 'y8best.pt' is in the same directory or provide the correct path.

# Read video source dynamically from a configuration file
try:
    with open("config/live_video_src.txt", "r") as file:
        video_source = file.read().strip()
        if not video_source:
            raise ValueError("Video source is empty. Please provide a valid source in the file.")
except FileNotFoundError:
    raise FileNotFoundError("The configuration file 'config/live_video_src.txt' was not found.")
except Exception as e:
    raise Exception(f"Error reading video source: {e}")

# Check if the video source is a webcam or a video file
if video_source.isdigit():
    video_source = int(video_source)  # Convert webcam index to integer for OpenCV

# Open video source
cap = cv2.VideoCapture(video_source)
if not cap.isOpened():
    raise Exception(f"Error: Unable to open video source '{video_source}'. Check the file path or webcam connection.")

# Process the video frame by frame
print("Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or unable to read frame.")
        break

    # Run YOLO detection on the current frame
    results = model.predict(source=frame, show=False)  # Show=False to use OpenCV for visualization
    annotated_frame = results[0].plot()  # Annotate the frame with YOLO detections

    # Display the frame with detections
    cv2.imshow("YOLO Detection Output", annotated_frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video source and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
