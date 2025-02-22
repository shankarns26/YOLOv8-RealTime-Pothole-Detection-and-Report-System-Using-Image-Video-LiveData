import subprocess
import os
import cv2
from ultralytics import YOLO

# Get the current script directory and set FFmpeg path
current_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(current_dir, "tools", "ffmpeg.exe")

# Verify FFmpeg exists
if not os.path.exists(ffmpeg_path):
    print(f"Warning: FFmpeg not found at {ffmpeg_path}")
    print("Please run download_ffmpeg.ps1 to install FFmpeg")
    # Try to find FFmpeg in system PATH
    ffmpeg_path = "ffmpeg.exe"

# Create required directories
os.makedirs('tools', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
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
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    size = (frame_width, frame_height)

    # Save processed frames to a high-quality temporary AVI file
    temp_output = "results/temp_output.avi"
    final_output = "results/processed_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    result_writer = cv2.VideoWriter(temp_output, fourcc, fps, size)

    print("Processing video frames...")
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame with YOLO
        results = model(frame)
        annotated_frame = results[0].plot()
        result_writer.write(annotated_frame)
        
        frame_count += 1
        if frame_count % 30 == 0:  # Update progress every 30 frames
            progress = (frame_count / total_frames) * 100
            print(f"Progress: {progress:.1f}%")

    cap.release()
    result_writer.release()

    # Use FFmpeg for high-quality video conversion
    print("Converting video to final format...")
    ffmpeg_cmd = [
        ffmpeg_path,
        "-i", temp_output,
        "-c:v", "libx264",
        "-preset", "slow",  # Higher quality encoding
        "-crf", "18",      # High quality (lower value = higher quality, range 0-51)
        "-movflags", "+faststart",  # Enable fast start for web playback
        "-y",              # Overwrite output file if it exists
        final_output
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
        print(f"Video processing completed. Output saved to {final_output}")
        # Clean up temporary file
        if os.path.exists(temp_output):
            os.remove(temp_output)
        return final_output
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg conversion: {e.stderr.decode()}")
        print("Keeping original output file as backup.")
        if os.path.exists(temp_output):
            return temp_output
        return None

# Example usage (this will be called in your Streamlit app)
if __name__ == '__main__':
    # Test detection from image
    detect_from_image('uploads/image.jpg', model)

    # Test detection from video
    detect_from_video('uploads/video.mp4', model)
