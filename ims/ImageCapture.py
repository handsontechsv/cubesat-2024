import cv2
import os
from picamera2 import Picamera2
import time
import requests
import json
from datetime import datetime
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-f", "--filename", help = "Image Filename")
 
# Read arguments from command line
args = parser.parse_args()


if args.filename:
    print("Displaying filename as: % s" % args.filename)
    filename = args.filename.strip()
else:
    filename = None

image_prefix = 'pi_'
image_suffix = '.jpg'
ImgOutput = "./pi"
key = 'resolutionValue'
url = 'http://localhost:5000/getResolution'
resolution = '800*600'
print (url)
try:
    myResponse = requests.get(url)
    if(myResponse.ok):
    
        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)
    
        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        resolution = jData[key]
    else:
      # If response code is not ok (200), print the resulting http error code with description
        #myResponse.raise_for_status()
        print("use default resolution.")
except Exception as e:
    print("call getResolution Error. use default resolution.")

print(resolution)
resValues = resolution.split('*')
IMG_SIZE=100
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (int(resValues[0]), int(resValues[1]))}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()

def capture_image(filename):
    #time.sleep(10)
    picam2.capture_file(ImgOutput + "/" + filename)
    #picam2.stop_()

if filename == None:
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H:%M:%S")
    filename = image_prefix + date_time + image_suffix

print(filename)    
capture_image(filename)
