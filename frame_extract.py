""" This is the frame extractor server which extracts the frames from footages"""
import os
import base64
from flask import Flask, request, jsonify
import cv2
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit

app = Flask(__name__)
cors = CORS(app)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

def allowed_file(filename):
    """
    This function defines the type of files allowed in the extraction
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@socketio.on('connect_with_FrameExtractor')
def handle_connect():
    """
    The function is triggered when a bidirectional connection
    is established between the frontend and this server.
    """
    print('Frontend connected to Frame Extractor Server.')


@app.route('/send-videos', methods=["POST"])
@cross_origin()
def extract_frames():
    """
    This function handles the incoming video file from the
    frontend and then saves it in uploads folder. It then returns
    an acknowledgement and the video path if the operation is successful.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return jsonify({'ack': True, 'filepath': filepath})

    return jsonify({'error': 'Invalid file format'})


@socketio.on("frame")
@cross_origin()
def extract_frames_from_video(video_path):
    """
    This function takes the video path from frontend through the
    socket channel and starts extracting the frames of footage using
    OpenCV. For each frame extracted, it returns the frame back to the frontend.
    """
    # pylint: disable=no-member
    cap = cv2.VideoCapture(video_path)
    # pylint: enable=no-member
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Convert frame to base64 for easy transmission
        # pylint: disable=no-member
        _, buffer = cv2.imencode('.jpg', frame)
        # pylint: enable=no-member
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        emit("extracted-frame", frame_base64)

    cap.release()
    return jsonify({'success':'Successful!'})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, debug=True)
