import subprocess
import os
import cv2
from ultralytics import YOLO

# Get the current script directory and set FFmpeg path
current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(current_dir, "ffmpeg.exe")

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

# Load the YOLOv8 model
model = YOLO(r"C:\Users\admin\Downloads\best (4).pt")

# Function to detect potholes in an image
def detect_from_image(image_path, model):
    image = cv2.imread(image_path) #read the image file 
    if image is None:
        print("Error: Cannot read the image.")
        return

    results = model(image)
    for result in results:
        annotated_image = result.plot()
        output_path = "results/image_result.jpg"
        cv2.imwrite(output_path, annotated_image)
        print(f"Annotated image saved to {output_path}")

# Function to detect potholes in a video
def detect_from_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (frame_width, frame_height)

    # Save directly to AVI format first (more reliable)
    temp_output = "results/temp_output.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    result_writer = cv2.VideoWriter(temp_output, fourcc, fps, size)

    print(f"Processing video...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        for result in results:
            annotated_frame = result.plot()
            result_writer.write(annotated_frame)

    cap.release()
    result_writer.release()

    # Convert to MP4 using cv2
    cap = cv2.VideoCapture(temp_output)
    output_path = "results/processed.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
    out = cv2.VideoWriter(output_path, fourcc, fps, size)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    cap.release()
    out.release()
    
    # Clean up temporary file
    if os.path.exists(temp_output):
        os.remove(temp_output)
    
    print(f"Video processing complete. Output saved to {output_path}")
    return output_path

# Example usage (this will be called in your Streamlit app)
if __name__ == '__main__':
    # Test detection from image
    detect_from_image('uploads/image.jpg', model)

    # Test detection from video
    detect_from_video('uploads/video.mp4', model)
