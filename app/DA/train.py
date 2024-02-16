from app.DA.face_recognition_package import recognition_module
import os
from flask import jsonify


facere = recognition_module.FaceRecognition()
class trainservice:
    
    @staticmethod
    def trainfolder(imggfolderpath_):
        images_train = [os.path.join(imggfolderpath_, filename) for filename in os.listdir(imggfolderpath_)]
        facere.face_encode(images_train)
        folder_name = os.path.basename(imggfolderpath_)
        company_number = folder_name.split('_')[0]
        pickle_file = f"{company_number}.pkl"
        facere.save_to_pickle(pickle_file)
    

# trainservice.trainfolder("C:/Users/LENOVO/Python-pod-tracer/tracer-backend/app/DA/3_Microsoft")