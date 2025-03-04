from flask import render_template, request, jsonify, url_for
import os
import cv2
import mediapipe as mp
import base64
import numpy as np
import time
from . import sign_language_bp

ASL_PATH = "static/ASL"
ISL_PATH = "static/ISL"
DETECTED_TEXT = ''

def get_sign_language_images(text, language):
    folder_path = ASL_PATH if language == "ASL" else ISL_PATH
    images = [url_for('static', filename=f"{language.upper()}/{letter}.jpg") 
              if os.path.exists(os.path.join(folder_path, f"{letter}.jpg")) else url_for('static', filename="placeholder.jpg")
              for letter in text.lower() if letter.isalpha() or letter.isdigit()]
    return images

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
recognizer_detected = None

@sign_language_bp.route('/sign_language')
def sign_language_home():
    return render_template('home.html')

@sign_language_bp.route('/translate', methods=['GET', 'POST'])
def translate():
    if request.method == 'GET':
        return render_template('trans.html')

    # Handle POST request
    text_input = request.form.get("text_input")
    speech_input = request.form.get("speech_input")
    language_choice = request.form.get("language")

    input_text = text_input if text_input else speech_input

    if input_text:
        images = get_sign_language_images(input_text, language_choice)
        return render_template('trans.html', images=images, input_text=input_text, language=language_choice)

    return render_template('trans.html', images=None)

@sign_language_bp.route('/process_frame', methods=['GET','POST'])
def process_frame():
    global DETECTED_TEXT
    if request.method == 'GET':
        return render_template('index.html')
    global recognizer_detected
    frame_timestamp_ms = int(time.time() * 1000)

    # Get the image data from the request
    data = request.json
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)

    np_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process the frame for gesture recognition
    recognizer.recognize_async(mp_image, frame_timestamp_ms)

    # Process hand landmarks
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display recognized gesture on the frame
    if recognizer_detected:
        cv2.putText(frame, recognizer_detected, (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
        DETECTED_TEXT=DETECTED_TEXT+recognizer_detected

    # Encode processed image for response
    ret, buffer = cv2.imencode('.jpg', frame)
    processed_image = base64.b64encode(buffer).decode('utf-8')
    
    return jsonify(result=recognizer_detected, image='data:image/jpeg;base64,' + processed_image)

@sign_language_bp.route('/predict', methods=['POST'])
def P_text():
    global DETECTED_TEXT
    if len(DETECTED_TEXT) > 0:
        temp = DETECTED_TEXT
        DETECTED_TEXT=''
        temp=predict_sentence(temp)
        print(temp)
        return jsonify(prediction=temp)
    else:
        return jsonify(prediction="No gestures recognized")