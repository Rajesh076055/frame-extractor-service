# frame-extractor-service

This Flask application serves as a frame extractor, utilizing OpenCV for image processing. It allows users to upload video files and extracts frames from them. The extracted frames can then be used for various purposes, such as analysis or further processing.

## Requirements

Make sure you have the following dependencies installed:

Flask==3.0.0
opencv-python==4.8.1.78
Flask-CORS==4.0.0
flask-socketio==5.3.6

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/Rajesh076055/frame-extractor-service.git
cd extractFrames-service
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Flask app:

```bash
python3 frame_extract.py
```

Open your web browser and navigate to http://localhost:5000/ to access the application.

Upload a video file through the provided form and submit.

The application will process the video, extract frames, and display the results.

## File Structure

frame_extract.py: Main Flask application file.
uploads/: Directory for storing uploaded video files.
