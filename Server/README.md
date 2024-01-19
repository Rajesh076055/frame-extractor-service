# frame-extractor-service

This Flask application serves as a frame extractor, utilizing OpenCV for image processing. It allows users to upload video files and extracts frames from them. The extracted frames can then be used for various purposes, such as analysis or further processing.

## Requirements

Make sure you have the following dependencies installed:

Flask==2.0.1
opencv-python==4.5.3.56
Flask-CORS==3.0.10
python-socketio==5.4.0

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

The application will process the video, extract frames, and return the results to the frontend. Just when the frontend recieves the frame, it sends it to ai for processing and ai returns frame back to frontend for displaying.

## File Structure

frame_extract.py: Main Flask application file.
uploads/: Directory for storing uploaded video files.
