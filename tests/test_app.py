import os
import tempfile
import pytest
from flask import Flask, jsonify
from werkzeug.datastructures import FileStorage
from Server.frame_extract import app  # Replace with the actual name of your module

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp() 
    client = app.test_client()

    yield client

def test_extract_frames_no_file_part(client):
    response = client.post('/send-videos')
    assert response.status_code == 404
    assert response.json == {'error': 'No file part'}

def test_extract_frames_no_selected_file(client):
    response = client.post('/send-videos', data={})
    assert response.status_code == 404
    assert response.json == {'error': 'No file part'}

def test_extract_frames_invalid_file_format(client):
    # Create a temporary file with an invalid format
    _, temp_file_path = tempfile.mkstemp(suffix='.exe')
    temp_file = FileStorage(stream=open(temp_file_path, 'rb'))

    response = client.post('/send-videos', data={'file': (temp_file, 'invalid_file.exe')})
    assert response.status_code == 403
    assert response.json == {'error': 'Invalid file format'}

    # Clean up the temporary file
    os.remove(temp_file_path)

def test_extract_frames_successful_upload(client):
    # Create a temporary file with a valid format
    temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', dir=app.config['UPLOAD_FOLDER'], delete=False)

    response = client.post('/send-videos', data={'file': (temp_file, 'valid_file.mp4')})
    assert response.status_code == 200
    assert response.json == {'ack': True, 'filepath': f'{app.config["UPLOAD_FOLDER"]}/valid_file.mp4'}

    # Clean up the temporary file
    os.remove(temp_file.name)
