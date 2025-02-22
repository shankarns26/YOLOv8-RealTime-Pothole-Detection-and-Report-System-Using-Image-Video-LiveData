# Pothole Detection System

A real-time pothole detection system using YOLOv8 and Streamlit, capable of processing images and videos with integrated location tracking and reporting features.

## System Requirements

1. **Hardware Requirements**:
   - Minimum 8GB RAM
   - CPU: Intel i5/AMD Ryzen 5 or better
   - GPU: Optional but recommended for faster detection
   - Storage: At least 5GB free space

2. **Software Requirements**:
   - Windows 10/11
   - Python 3.8 or higher
   - Git (optional, for cloning repository)
   - PowerShell 5.0 or higher

## Complete Setup and Running Guide

### Step 1: Setup Virtual Environment
```powershell
# Navigate to your project directory
cd "c:\Users\admin\Downloads\pothole for dk\pothole for dk"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### Step 2: Install Dependencies
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### Step 3: Install FFmpeg
```powershell
# Run the FFmpeg installation script
powershell -ExecutionPolicy Bypass -File download_ffmpeg.ps1

# Verify FFmpeg installation
.\tools\ffmpeg.exe -version
```

### Step 4: Check Directory Structure
Make sure these directories exist:
```powershell
# Create directories if they don't exist
mkdir tools -ErrorAction SilentlyContinue
mkdir uploads -ErrorAction SilentlyContinue
mkdir results -ErrorAction SilentlyContinue
```

### Step 5: Verify Model Path
Check if the YOLO model path in `app.py` is correct:
```python
model = YOLO(r"C:\Users\admin\Downloads\best (4).pt")
```
Make sure this file exists at the specified location.

### Step 6: Run the Application
```powershell
# Make sure you're in the virtual environment (should see (venv) in terminal)
streamlit run app.py
```

## Using the Application

### 1. Image Detection
- Click "Using Image" in sidebar
- Choose "Upload Image" or "Open Camera"
- Upload an image or take a photo
- Wait for detection results
- Fill in pothole information
- Click "Submit Report"

### 2. Video Detection
- Click "Using Video" in sidebar
- Choose "Upload Video"
- Upload a video file (mp4, mkv, or avi)
- Wait for processing (this may take time)
- Review the detection results
- Fill in pothole information
- Click "Submit Report"

### 3. Live Camera
- Click "Live Camera" in sidebar
- Allow camera access if prompted
- Point camera at potholes
- Detection happens in real-time

## Troubleshooting Guide

### 1. FFmpeg Issues
```powershell
# If FFmpeg not found, reinstall:
powershell -ExecutionPolicy Bypass -File download_ffmpeg.ps1

# Verify installation:
.\tools\ffmpeg.exe -version
```

### 2. Python Dependencies Issues
```powershell
# Reinstall all packages
pip install -r requirements.txt --force-reinstall

# Check installed packages
pip list
```

### 3. Streamlit Startup Issues
```powershell
# Deactivate and reactivate virtual environment
deactivate
.\venv\Scripts\activate

# Then try running again
streamlit run app.py
```

### 4. Video Processing Issues
- Try using smaller video files
- Ensure sufficient disk space
- Close resource-intensive applications
- Check supported formats (mp4, mkv, avi)

## Quick Commands Reference

```powershell
# Start application
streamlit run app.py

# Check FFmpeg
.\tools\ffmpeg.exe -version

# Check Python version
python --version

# Check installed packages
pip list

# Stop the application
# Press Ctrl+C in terminal

# Deactivate virtual environment when done
deactivate
```

## Best Practices

### 1. Environment Management
- Always use the virtual environment
- Keep dependencies updated
- Clean up environment when switching projects

### 2. File Management
- Regularly clean uploads folder
- Remove processed results when not needed
- Maintain organized project structure

### 3. Detection Quality
- Ensure good lighting conditions
- Keep camera steady during capture
- Maintain clear view of potholes
- Use supported video formats

### 4. System Resources
- Close unnecessary applications
- Monitor disk space
- Keep system updated
- Check CPU/GPU usage

## Support and Maintenance

### Regular Maintenance
1. Update Python packages:
   ```powershell
   pip install --upgrade -r requirements.txt
   ```

2. Clean directories:
   ```powershell
   # Remove temporary files
   Remove-Item uploads\* -Force
   Remove-Item results\* -Force
   ```

3. Update FFmpeg:
   - Run download_ffmpeg.ps1 periodically
   - Check for version updates

### Getting Help
1. Check error messages in terminal
2. Verify file paths and permissions
3. Ensure all dependencies are installed
4. Monitor system resources
5. Check application logs

## License

This project is licensed under the MIT License - see the LICENSE file for details.