import cv2
import time
from ultralytics import YOLO

# Load your YOLO model (provide the correct path to the trained weights)
model = YOLO(r"C:\Users\admin\Downloads\best (4).pt")  # Adjust as necessary

# Initialize video capture (0 for the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

print("Starting live pothole detection. Press 'q' to quit.")

# Create window with specific properties
window_name = 'Live Pothole Detection'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Set window to be always on top and set initial size
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
cv2.resizeWindow(window_name, 800, 600)
cv2.moveWindow(window_name, 100, 100)  # Position window at (100,100)

# Main loop for live detection
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from the camera.")
        break

    # Run YOLO model on the frame
    results = model(frame)
    
    # Draw the results on the frame
    for result in results:
        annotated_frame = result.plot()
        
        # Add text showing this is live detection
        cv2.putText(annotated_frame, "Live Pothole Detection", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the annotated frame
        cv2.imshow(window_name, annotated_frame)
        
        # Keep window on top
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        
        # Convert BGR to RGB for Streamlit
        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Yield the frame to Streamlit
        yield rgb_frame
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Detection stopped.")
