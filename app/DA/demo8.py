import base64
import cv2
import numpy as np
from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
import io
from PIL import Image
from app.DA.face_recognition_package import recognition_module
from ultralytics import YOLO
import math
import os
import time



# Set confidence threshold for object detection
confidence = 0.6

# Initialize YOLO model with pre-trained weights
model = YOLO('app/DA/models/best.pt')

# Define class names for detected objects
classNames = ["fake", "real"]

# app = Flask(__name__)
# CORS(app, origins="*")

facere = recognition_module.FaceRecognition()

fraudBp = Blueprint('fraud_bp', __name__)

@fraudBp.route('/capture_and_process', methods=['POST'])
def capture_and_process():
    im_b64 = request.json['image']
    org_id = request.json["org_id"]
    event_id = request.json["event_id"]
    device_id = request.json["device_id"]
    #print(org_id)

    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    results = model(img)

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    print('img shape', img_arr.shape)

    img_path = 'captured_image.jpg'
    cv2.imwrite(img_path, img_arr)
    model_path = f'C:/Users/LENOVO/Python-pod-tracer/tracer-backend/app/DA/face_recognition_package/{org_id}.pkl'
    #  "C:\Users\LENOVO\Python-pod-tracer\tracer-backend\app\DA"
    facere.load_from_pickle(model_path)
    

    resp = facere.face_test(img_path, event_id, device_id)
    print(resp)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract confidence and class information
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            # Check if the confidence exceeds the threshold
            if conf > confidence:
                classification_result = classNames[cls]
                print(f"Object detection result: {classification_result}")
            else:
                print(f"Object detection result: Fake ")
                # Create 'fake' folder if not present
                fake_folder = 'fake'
                if not os.path.exists(fake_folder):
                    os.makedirs(fake_folder)

                # Save the image in the 'fake' folder
                fake_image_path = os.path.join(fake_folder, f"fake_image_{int(time.time())}.jpg")
                cv2.imwrite(fake_image_path, img_arr)
                print(f"Saved fake image: {fake_image_path}")

    #if resp is not None:
    return resp
    # else:
    #     return jsonify({'result': 'No match found'})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
