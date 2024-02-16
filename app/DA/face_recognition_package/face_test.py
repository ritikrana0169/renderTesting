from flask import Flask, render_template, request
import recognition_module
import numpy as np
import cv2
import base64
app = Flask(__name__)
face_recognition = recognition_module.FaceRecognition()
#@app.route('/face_test', methods=['POST'])
def test_face():
    try:
        # Get the uploaded image from the request
        data = request.get_json()
        frame_as_text = data.get('file')  # Retrieve the frame data from 'file' key

        # Decode the base64 encoded frame
        decoded_frame = base64.b64decode(frame_as_text)
        nparr = np.frombuffer(decoded_frame, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform face testing using the received frame
        # Use 'frame' for face recognition processing
        face_recognition.face_test(frame)
        
        return "Face test completed successfully"
    except Exception as e:
        return str(e)

#  if __name__ == '__main__':
#      app.run(debug=True, host='0.0.0.0', port=5000)