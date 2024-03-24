#!/usr/bin/env python3

import os
from PIL import Image, ImageStat
import shutil
import argparse

# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-s", "--sourcedir", help = "Image files directory")
parser.add_argument("-t", "--dupdir", help = "duplicate Image files directory")
parser.add_argument("-dt", "--diffthreshold", help = "duplicate Image files directory")
 
# Read arguments from command line
args = parser.parse_args()

if args.sourcedir:
    print("Displaying source dir as: % s" % args.sourcedir)
    image_folder = args.sourcedir.strip()
else:
    image_folder = r'pi' 
    
if args.dupdir:
    print("Displaying duplicate dir as: % s" % args.dupdir)
    duplicate_folder = args.dupdir.strip()
else:
    duplicate_folder = r'duplicate'   

if args.diffthreshold:
    print("Displaying diffthreshold as: % s" % args.diffthreshold)
    diff_threshold = int(args.diffthreshold.strip())
else:
    diff_threshold = 5    


'''
The script takes the RMS value of an image and compares it to another image's RMS value. If the difference between the two images is less than 1 (calculated in the function 'average_diff') then the images are considered the same, and the duplicate is moved to the duplicates folder.
'''

image_files = []
rms_pixels = []

# create directory for duplicates if it does not exist
if not os.path.exists(duplicate_folder):
    os.makedirs(duplicate_folder)

#Function calculates the difference between the CURRENT image file RMS value and RMS values calculated at start

def average_diff(v1, v2):
    duplicate = False
    calculated_rms_difference = [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]
    if calculated_rms_difference[0] < diff_threshold and calculated_rms_difference[0] > -diff_threshold and calculated_rms_difference[1] < diff_threshold and calculated_rms_difference[1] > -diff_threshold and calculated_rms_difference[2] < diff_threshold and calculated_rms_difference[2] > -diff_threshold:
        duplicate = True
    return duplicate

def quick_rms(images, rms):
    image_file_count = 0
    while image_file_count < len(images):
        image_file = images[image_file_count]
        check_duplicates = image_file.endswith('.jpg')
        if check_duplicates:
            rms_file_count = 1
            original_image = Image.open(os.path.join(image_folder, image_file))
            rms_original = ImageStat.Stat(original_image).mean
            while rms_file_count < len(rms):
                rms_file = rms[rms_file_count]
                duplicate_image = average_diff(rms_original, rms_file)
                print('Checking: ', image_file_count, 'against', rms_file_count, 'of', len(rms), end='\r', flush=False)
                if image_file != rms_file[3]:
                    if duplicate_image:
                        print(image_file)
                        source = os.path.join(image_folder, rms_file[3])
                        dest = os.path.join(duplicate_folder, rms_file[3])
                        shutil.move(source, dest)
                        image_to_remove = rms_file[3]
                        images.remove(image_to_remove)
                        rms.remove(rms_file)
                        print('MOVED to ' +  duplicate_folder + ':' + image_to_remove) # comment this out when in production environment
                rms_file_count += 1
        image_file_count += 1
    return
#Creates a list of images to be checked and compared, these are the images stored in the Image folder at top of script
for x in os.listdir(image_folder):
    image_files.append(x)
#Create a list with all the Image RMS values. These are used to compare to the CURRENT image file in list
for x in image_files:
    if x.endswith('.jpg'):
        compare_image = Image.open(os.path.join(image_folder, x))
        rms_pixel = ImageStat.Stat(compare_image).mean
        rms_pixel.append(x)
        rms_pixels.append(rms_pixel)
        print(rms_pixel)
#Driver code, runs the script
quick_rms(image_files, rms_pixels)