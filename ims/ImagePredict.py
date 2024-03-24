import joblib
import numpy
import pandas as pd
import cv2
import os
from tqdm import tqdm
from sklearn.cluster import KMeans
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import colorsys
import json
from json import JSONEncoder
from rembg import remove
import pickle
from picamera2 import Picamera2, Preview
import time
import cv2
import opencv_jupyter_ui as jcv2
import requests
import json
from pathlib import Path


IMG_DIR = "pi"
MODEL_FILE='color_svm_9_3.sav'
IMG_SIZE=50
metadata_suffix = '_metadata.json'
predict_field_name = 'predict'

def save_predict_result(file_path,result):
    if Path(file_path).exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
            data[predict_field_name] = str(result)
            save_metadata(file_path,data)
    else:
        print("metadata does not exist, create metadata file and save predict result.")
        data = {predict_field_name:str(result)}
        save_metadata(file_path,data)
        
def get_predict(file_path):
    if Path(file_path).exists():
        with open(file_path, 'r') as file:
            data = json.load(file)
            if predict_field_name in data:
                return True
            else:
                return False
    else:
        print("metadata does not exist, return False.")
        return False
        
def get_files_by_extension(path, extension):
    file_list = []
    for file_name in os.listdir(path):
        if file_name.endswith(extension):
            file_list.append(file_name)
    return file_list

def save_metadata(filename,metadata):
    if metadata != None:
        with open(filename, "w") as f: 
            json.dump(metadata, f, indent=2)  # The indent parameter is optional and adds formatting for better readability

def get_image(image_path):
    image = cv2.imread(image_path)
    w = image.shape[1]
    new_w = IMG_SIZE
    new_h = int(image.shape[0]/(image.shape[1]/IMG_SIZE))
    
    new_image=cv2.resize(image,(new_w,new_h))
    new_image = remove(new_image)
    new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    return new_image


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def extract_features(path, img, split_tup):
    image_path = os.path.join(path, img)
    json_file = split_tup[0] + ".json"
    json_path = os.path.join(path, json_file)
    if os.path.exists(json_path):
        # Opening JSON file
        f = open(json_path)
        json_details = json.load(f)
        hsl_color_values = json_details["hsl_color_values"]
        return hsl_color_values
    else:
        image = get_image(image_path)
        number_of_colors = 10
        modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
        nobg_image = remove(modified_image)
        clf = KMeans(n_clusters = number_of_colors)
        labels = clf.fit_predict(modified_image)
        
        counts = Counter(labels)

        center_colors = clf.cluster_centers_

        # We get ordered colors by iterating through the keys
        ordered_colors = [center_colors[i] for i in counts.keys()]
        hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]
        hsl_color_values = []

        for i in range(len(rgb_colors)):
            rgb_color = rgb_colors[i]
            hsl_color_val = colorsys.rgb_to_hsv(rgb_color[0],rgb_color[1],rgb_color[2])
            hsl_color_values.append(hsl_color_val)

        
        json_details = {"rgb_colors": rgb_colors,
                        "hex_colors": hex_colors,
                        "hsl_color_values": hsl_color_values}
        # Serializing json
        json_object = json.dumps(json_details, indent=4, cls=NumpyArrayEncoder)
 
        # Writing to sample.json
        with open(json_path, "w") as outfile:
            outfile.write(json_object)

        return hsl_color_values

# Load the pre-trained SVM model from the .sav file
model = joblib.load(MODEL_FILE)

# Define a function to make predictions using the pre-trained model
def predict(path, img):
    split_tup = os.path.splitext(img)
    if len(split_tup) > 1 and split_tup[len(split_tup)-1] == ".jpg": 
        features = extract_features(path, img, split_tup)
        # Convert input data to a numpy array
        input_data = numpy.array(features).reshape(1, -1)
        input_data = input_data/255
        # Make a prediction using the pre-trained model
        prediction = model.predict(input_data)
        #print prediction data
        #print(prediction)
        # Return the predicted output
        return prediction[0]
    else:
        print("The image file is not JPG file")

           

try:
    files = get_files_by_extension(IMG_DIR,'.jpg') 
    for f in files:
        base_name, _ = os.path.splitext(f)
        metadata_filename = IMG_DIR + '/'+ base_name.strip() + metadata_suffix
        predicted = get_predict(metadata_filename)
        if not(predicted):
            print("predicting image "+ f)
            predict_result = predict(IMG_DIR,f)
            print(predict_result)
            save_predict_result(metadata_filename,predict_result)    
except Exception as e:
        print('error')



