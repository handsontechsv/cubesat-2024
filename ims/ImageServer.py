from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
from datetime import datetime
import json
import asyncio

app = Flask(__name__)

IMAGE_DIRECTORY = 'pi'

metadata_suffix = '_metadata.json'

async def run_subprocess(command):
    # Create a subprocess using asyncio.subprocess
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for the subprocess to complete
    stdout, stderr = await process.communicate()

    # Print the output
    print(f"Command: {command}")
    if process.returncode == 0:
        print(f"Success! Output:\n{stdout.decode()}")
    else:
        print(f"Error! Return code: {process.returncode}\n{stderr.decode()}")

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

@app.route('/imageCapture', methods=['POST'])
def call_external_program():
    # Get the raw body of the POST request
    raw_data = request.data
    # If the data is JSON, you can parse it using request.get_json()
    json_data = request.get_json()
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    image_filename = "pi" + date_time + ".jpg"
    metadata_filename = IMAGE_DIRECTORY + "/pi" + date_time + metadata_suffix
    save_metadata(metadata_filename,json_data)
    capture_image_parameter = '-f ' + image_filename
    try:
        result = subprocess.check_output(['python3', 'ImageCapture.py',capture_image_parameter], universal_newlines=True)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error_message': str(e)})


@app.route('/downloadImage', methods=['GET'])
def download_image():
    # Get the filename from the request parameters
    filename = request.args.get('filename')

    # Check if the filename is provided
    if not filename:
        return jsonify({'error': 'Please provide a filename parameter.'})

    # Check if the file exists in the specified directory
    image_path = os.path.join(IMAGE_DIRECTORY, filename)
    if not os.path.exists(image_path):
        return jsonify({'error': 'File not found.'})

    # Send the file for download
    return send_from_directory(IMAGE_DIRECTORY, filename, as_attachment=True)

@app.route('/listFiles', methods=['GET'])
def list_files():
    # Get the list of files in the specified directory
    try:
        files = [f for f in os.listdir(IMAGE_DIRECTORY) if os.path.isfile(os.path.join(IMAGE_DIRECTORY, f))]
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': f'Error listing files: {str(e)}'})

@app.route('/listImages', methods=['GET'])
def list_images():
    # Get the list of files in the specified directory
    try:
        files = get_files_by_extension(IMAGE_DIRECTORY,'.jpg')
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': f'Error listing files: {str(e)}'})


@app.route('/setResolution', methods=['GET'])
def setResolution():
    # Get parameters from the request
    param1 = request.args.get('resolution')

    # Validate parameters (optional)
    if param1 is None:
        return jsonify({'error': 'Missing parameters'}), 400

    # Process parameters (you can perform any logic here)
    result = param1
    filename = 'resolution.txt'
    with open(filename, 'w') as f:
        f.write(result)
    f.close()

    with open(filename, "r") as file:
        data = file.read()
        result = data
        print(data)

    # Return the result as JSON
    return jsonify({'resolutionValue': result})

@app.route('/getResolution', methods=['GET'])
def getResolution():
    filename = 'resolution.txt'
    with open(filename, "r") as file:
        data = file.read()
        result = data
        print(data)

    # Return the result as JSON
    return jsonify({'resolutionValue': result})


@app.route('/predict', methods=['POST'])
async def predict():
     try:
        # Specify the command you want to run asynchronously
        command = "python3 ImagePredict.py"  # Replace this with your desired command
        # Run the subprocess asynchronously
        await run_subprocess(command)
        return jsonify({'status': 'predict triggered'})
     except Exception as e:
        return jsonify({'status': 'error', 'error_message': str(e)})

def update_json_file(file_path,jsonObj):
    print(file_path)
    data = {}
    if Path(file_path).exists():
        with open(file_path, 'r') as file:
            data = json.load(file)               
    for key, value in jsonObj:
        data[key] = str(value)
    save_metadata(file_path,data)

@app.route('/editMetadata', methods=['POST'])
def editMetadata():
     try:
        # Specify the command you want to run asynchronously
        filename = request.args.get('filename')
        metadata_filename = IMAGE_DIRECTORY + "/"+ filename
        print(metadata_filename)
        # If the data is JSON, you can parse it using request.get_json()
        json_data = request.get_json()
        update_json_file(metadata_filename,json_data)
        return jsonify({'status': 'update metadata successfully'})
     except Exception as e:
        return jsonify({'status': 'error', 'error_message': str(e)})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)





