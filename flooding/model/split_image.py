import os

from PIL import Image
from pathlib import Path


def split_image(input_image_path, output_folder):
    # Open the input image
    original_image = Image.open(input_image_path)

    # Get the size of the original image
    width, height = original_image.size

    # Calculate the number of rows and columns for the 16x16 grid
    rows = height // 32
    cols = width // 32

    base_file_name = Path(os.path.basename(input_image_path)).stem
    # Loop through each grid cell
    for row in range(rows):
        for col in range(cols):
            # Calculate the coordinates for cropping each cell
            left = col * 32
            top = row * 32
            right = left + 32
            bottom = top + 32

            # Crop the cell from the original image
            cell_image = original_image.crop((left, top, right, bottom))

            # Save the cropped cell to the output folder
            cell_image.save(f"{output_folder}/{base_file_name}_{row}_{col}.png")

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    files = os.listdir(input_folder)

    # Filter only PNG files
    png_files = [file for file in files if file.lower().endswith(".png")]

    # Loop through each PNG file
    for png_file in png_files:
        # Construct the full path for the input image
        input_image_path = os.path.join(input_folder, png_file)

        image_output_path = os.path.join(output_folder, png_file)
        os.makedirs(image_output_path, exist_ok=True)

        split_image(input_image_path, image_output_path)

if __name__ == "__main__":
    # Replace 'input_image.png' with the path to your PNG image
    input_image_path = "simple"

    # Replace 'output_folder' with the desired output folder path
    output_folder = "small"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Split the image and save the small cells
    process_images(input_image_path, output_folder)