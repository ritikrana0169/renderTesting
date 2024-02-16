import face_recognition as fr
import cv2
import os
import numpy as np
import pandas as pd
import pickle
from flask import Flask, jsonify #added
from app.services.admin_attendance_mark_service import mark_attendance

class FaceRecognition:
    def __init__(self):
        self.encodeImg_list = []
        self.encodeNames_list = []
    def face_encode(self,train_images_folder):
        for image in train_images_folder:
            #Loading the current image
            currImage = fr.load_image_file(image)
            currImage_rgb = cv2.cvtColor(currImage, cv2.COLOR_RGB2BGR)
            try:
                #Finding the face locations
                locations=fr.face_locations(currImage_rgb)
                #Encoding the current Face
                encode_Img=fr.face_encodings(currImage_rgb,locations,model='hog')
                #Storing the encoded array into the list
                self.encodeImg_list.append(encode_Img[0])
                #manually extracting the file names
                self.encodeNames_list.append(str(image)[str(image).rfind('\\')+1:].split('_')[0])
            except:
                print("Face not found")
    def face_test(self, image, event_id, device_id):
        #Loading the test image
        currImg = fr.load_image_file(image)                            
        currImg_rgb = cv2.cvtColor(currImg,cv2.COLOR_BGR2RGB)
        try:
            #Extracting the face locations
            locations=fr.face_locations(currImg_rgb)
            #encoding the test image and extracting the list
            test_encode = fr.face_encodings(currImg_rgb,locations,model='hog')[0]
            for encode,name in zip(self.encodeImg_list,self.encodeNames_list):
                #if the currentEncode is match with one encode which is present in the final_list
                if fr.compare_faces([encode],test_encode,tolerance=0.5)[0]:

                    # mark attendance function call
                    # print("Passing " + event_id + " device: " + device_id)
                    mark_attendance(name, event_id, device_id)

                    print("Match found with ",name)
                    result="Match found with " + name#added
                    return jsonify({'message': result}), 200#added
                    #Testing the distance between the training image and matching image
                    print(fr.face_distance([encode],test_encode))
                    break
            else:
                print("No match found")
                return jsonify({'message':"no match found....."}), 404 #added
        except Exception as e:
            #print(str(e))  #removed
            return jsonify({'message': 'something went wrong'}), 500 #added
    #Getting pickle file name dynamically
    def pickle_name(self,organization_code):
        self.organization_code=organization_code
        return organization_code
    #Saving the model into pickle
    def save_to_pickle(self, pickle_file):
        data = {'encodeImg_list': self.encodeImg_list,
                'encodeNames_list': self.encodeNames_list}
        full_path = r'C:\Users\LENOVO\Python-pod-tracer\tracer-backend\app\DA\face_recognition_package\{}'.format(pickle_file)

        with open(full_path, 'wb') as file:
            pickle.dump(data, file)
    #Loading the model from pickle
    def load_from_pickle(self,pickle_file):
        try:
            with open(pickle_file,'rb') as file:
                data=pickle.load(file)
                self.encodeImg_list=(data['encodeImg_list'])
                self.encodeNames_list=(data['encodeNames_list'])
            print("Loaded successfully")
        except Exception as e:
            print(str(e))
    #Updating the model
    def update_pickle(self,new_train_folder,pickle_file):
        #Load existing data
        self.load_from_pickle(pickle_file)
        self.face_encode(new_train_folder)
        self.save_to_pickle(pickle_file)
#Instantiating the FaceRecognition class
# face_recognition=FaceRecognition()
#Training
# # Path for the training images
# train_folder_path='C:\\Users\\ommah\\OneDrive\\Desktop\\Fraud\\9001'
# images_train=[os.path.join(train_folder_path,filename) for filename in os.listdir(train_folder_path)]
# face_recognition.face_encode(images_train)
# # Saving the encoded faces and names to a pickle file
# company_name = os.path.basename(train_folder_path)
# pickle_file = f"{company_name}.pkl"
# face_recognition.save_to_pickle(pickle_file)
# Loading and testing
# pickleFile=face_recognition.pickle_name(9001)
# face_recognition.load_from_pickle(f"{pickleFile}.pkl")
# test_image_path='C:\\Users\\ommah\\OneDrive\\Desktop\\Fraud\\abdultest.png'
# face_recognition.face_test(test_image_path)
# #Updating
# update_folder='D:/Update'
# pickle_file="encoded_faces.pkl"
# update_images=[os.path.join(update_folder,filename) for filename in os.listdir(update_folder)]
# face_recognition.update_pickle(update_images,pickle_file)







#Path for the testing images
# test_folder_path='D:/Face_Capture/Test_images'
# images_test=[os.path.join(test_folder_path,filename) for filename in os.listdir(test_folder_path)]
# for image in images_test:
#     face_recognition.face_test(image)
# df=pd.DataFrame({'Actual Images':face_recognition.Actual_Images,
#               'Predicted Images':face_recognition.Predicted_Images,
#               'Predicted Score':face_recognition.Predicted_score})
# df.to_excel("output.xlsx")
# output=pd.read_excel("output.xlsx")
# print(output)



