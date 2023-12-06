from flask import Flask, request, jsonify
import cv2
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import base64
from flask_socketio import SocketIO, emit
import time

app = Flask(__name__)
cors = CORS(app)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', 'Hello from server!')


@app.route('/send-videos', methods=["POST"])
@cross_origin()
def extract_frames():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # emit("frame", frames)

        return jsonify({'ack': True, 'filepath': filepath})

    return jsonify({'error': 'Invalid file format'})


@socketio.on("frame")
@cross_origin()
def extract_frames_from_video(video_path):

    cap = cv2.VideoCapture(video_path)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # Convert frame to base64 for easy transmission
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        # frames.append(frame_base64)

        emit("extracted-frame", frame_base64)

    cap.release()
    # print(frames);


# def acknowledgement(ack):
#     print(ack)


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    socketio.run(app, debug=True)
