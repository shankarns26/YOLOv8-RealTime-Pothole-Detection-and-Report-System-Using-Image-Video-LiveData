import streamlit as st
import pandas as pd
import geocoder
import os
from PIL import Image
from mail import send_email
from ultralytics import YOLO
from pothole_detection import detect_from_image, detect_from_video
import streamlit.components.v1 as components
import subprocess
import cv2
import time

os.makedirs('uploads', exist_ok=True) #it helps to create the directory of it exist it won't throw any error

# Initialize YOLOv8 model (replace with the correct path to your trained model)
model = YOLO(r"C:\Users\admin\Downloads\best (4).pt")
# Sidebar menu
page = st.sidebar.selectbox("Pages Menu", options=['Home', 'Using Image', 'Using Video', 'Live Camera']) #selected option stored page

# Function to register pothole information
def register(location, highway_type, size, position, is_video=False):
    data = {"location": location, "highway_type": highway_type, "size": size, "position": position}
    send_email(data, 'siddeshshankar1@gmail.com', is_video)  
    st.info("Reported successfully.")

# Geolocation (fallback to IP-based geolocation)
def get_fallback_location():
    g = geocoder.ip('me') #get the device's public IP address
    if g.latlng:
        return g.latlng
    else:
        return [0, 0]  # Default location

# Function to display map and gather pothole information
def get_pothole_info():
    location = get_fallback_location()
    st.sidebar.markdown("---")

    
    df = pd.DataFrame([location], columns=['lat', 'lon'])
    st.info(f"Location: Latitude {location[0]}, Longitude {location[1]}")

    # Gather additional information about the pothole
    highway_type = st.sidebar.selectbox("Select Road Type:", options=["National Highway", "Local Road"])
    size = st.sidebar.selectbox("Approx. Size of Pothole", options=["Small Pothole", "Medium Pothole", "Large Pothole"])
    position = st.sidebar.selectbox("Position of Pothole", options=["Center", "Sideways"])
    
    return location, highway_type, size, position

# Function to load and save uploaded image
def load_image(image_file):
    img = Image.open(image_file)
    img.save("uploads/image.jpg")
    return img

# Function to load and save uploaded video
def load_video(video_file):
    path_name = "uploads/video.mp4"
    with open(path_name, 'wb') as f:
        f.write(video_file.read()) #read and write in the binary formate to specified path

# Page: Using Image
if page == 'Using Image':
    st.title("Pothole Detection Using Image")
    choice_upload = st.sidebar.selectbox("Select a Method", options=['Upload Image', 'Open Camera'])
    if choice_upload == 'Upload Image':
        image_file = st.file_uploader('Upload Image', type=['png', 'jpg', 'jpeg'])
        if image_file is not None:
            col1, col2 = st.columns(2)
            file_details = {"filename": image_file.name, "filetype": image_file.type, "filesize": image_file.size}
            st.write(file_details)
            col1.image(load_image(image_file))
            detect_from_image("uploads/image.jpg", model)  # Pass the YOLOv8 model here
            col2.image("results/image_result.jpg")
            location, highway_type, size, position = get_pothole_info()
            if st.sidebar.button("Submit Report"):
                register(location, highway_type, size, position)

    elif choice_upload == 'Open Camera':
        img_file_buffer = st.camera_input("Take a picture")
        if img_file_buffer is not None:
            img = Image.open(img_file_buffer)
            img.save("uploads/image.jpg")
            detect_from_image("uploads/image.jpg", model)  # Pass the YOLOv8 model here
            st.image("results/image_result.jpg")
            location, highway_type, size, position = get_pothole_info()
            if st.sidebar.button("Submit Report"):
                register(location, highway_type, size, position)

# Page: Using Video
elif page == 'Using Video':
    st.title("Pothole Detection Using Video")
    video_option = st.sidebar.selectbox("Select a Method", options=["Upload Video", "Live Video"])

    if video_option == "Upload Video":
        video_file = st.file_uploader("Upload Video", type=["mp4", "mkv", "avi"])
        if video_file is not None:
            with st.spinner("Processing video... Please wait."):
                # Save uploaded video
                load_video(video_file)
                
                try:
                    # Process video and get output path
                    output_path = detect_from_video("uploads/video.mp4", model)
                    
                    if os.path.exists(output_path):
                        st.success("Video processing complete!")
                        st.snow()
                        
                        # Display original video
                        st.subheader("Processed Video (with Pothole Detection)")
                        st.video(video_file)
                        
                        # Get pothole information
                        location, highway_type, size, position = get_pothole_info()
                        if st.sidebar.button("Submit Report"):
                            register(location, highway_type, size, position, is_video=True)
                    else:
                        st.error("Error: Processed video file not found.")
                except Exception as e:
                    st.error(f"Error processing video: {str(e)}")

    elif video_option == "Live Video":
        st.title("Live Video Detection")
        
        if 'video_camera_running' not in st.session_state:
            st.session_state.video_camera_running = False

        # Camera controls
        col1, col2 = st.columns(2)
        with col1:
            start_button = st.button("Start Live Detection", type="primary")
        with col2:
            stop_button = st.button("Stop Live Detection", type="secondary")

        if start_button:
            st.session_state.video_camera_running = True
            st.success("Live detection started! You should see the camera feed below.")

        if stop_button:
            st.session_state.video_camera_running = False
            st.warning("Live detection stopped.")

        # Main content area for camera feed
        if not st.session_state.video_camera_running:
            st.info("Click 'Start Live Detection' to begin.")
            
        if st.session_state.video_camera_running:
            try:
                stframe = st.empty()
                cap = cv2.VideoCapture(0)
                
                if not cap.isOpened():
                    st.error("Could not access the camera. Please make sure it's connected and not in use by another application.")
                    st.session_state.video_camera_running = False
                else:
                    st.markdown("### Live Detection Feed")
                    while st.session_state.video_camera_running:
                        ret, frame = cap.read()
                        if ret:
                            # Run detection on the frame
                            results = model(frame)
                            
                            # Draw the results on the frame
                            for result in results:
                                annotated_frame = result.plot()
                                
                                # Convert BGR to RGB for Streamlit
                                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                                
                                # Display the frame in Streamlit
                                stframe.image(rgb_frame, channels="RGB", use_column_width=True)
                        else:
                            st.error("Failed to read from camera")
                            break

                cap.release()
                stframe.empty()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.video_camera_running = False

# Page: Live Camera
elif page == 'Live Camera':
    st.title("Pothole Detection Using Live Camera")
    
    if 'camera_running' not in st.session_state:
        st.session_state.camera_running = False

    # Camera controls in sidebar
    st.sidebar.markdown("### Camera Controls")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_button = st.button("Start Camera", type="primary")
    with col2:
        stop_button = st.button("Stop Camera", type="secondary")

    if start_button:
        st.session_state.camera_running = True
        st.success("Camera started! You should see the live feed below.")

    if stop_button:
        st.session_state.camera_running = False
        st.warning("Camera stopped.")

    # Main content area for camera feed
    if not st.session_state.camera_running:
        st.info("Click 'Start Camera' to begin live pothole detection.")
        
    if st.session_state.camera_running:
        try:
            stframe = st.empty()
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("Could not access the camera. Please make sure it's connected and not in use by another application.")
                st.session_state.camera_running = False
            else:
                st.markdown("### Live Detection Feed")
                while st.session_state.camera_running:
                    ret, frame = cap.read()
                    if ret:
                        # Run detection on the frame
                        results = model(frame)
                        
                        # Draw the results on the frame
                        for result in results:
                            annotated_frame = result.plot()
                            
                            # Add timestamp
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            cv2.putText(annotated_frame, timestamp, (10, 30), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                            
                            # Convert BGR to RGB for Streamlit
                            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                            
                            # Display the frame in Streamlit
                            stframe.image(rgb_frame, channels="RGB", use_column_width=True)
                    else:
                        st.error("Failed to read from camera")
                        break

            cap.release()
            stframe.empty()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.camera_running = False

# Page: Home
else:
    st.title('Pothole Detection')
    st.markdown("> Select any choice from the sidebar to proceed")
    st.image("image1.jpeg")
    st.markdown(""" ## Detecting Potholes on Road using YOLOv8 Model
    Features:
    - Detects Potholes From Images
    - Detects Potholes Using Live Camera Feed
    - Detects Potholes From Uploaded Videos
    - Reports Pothole Data through email
    - Automatically Retrieves Location Information via IP Address           
    """)