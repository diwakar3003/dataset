import os
from PIL import Image

def tiff_to_png_and_rotate(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all TIFF files in the input folder
    tiff_files = [f for f in os.listdir(input_folder) if f.endswith('.tiff')]

    # Convert each TIFF file to PNG and rotate by 90 degrees clockwise
    for tiff_file in tiff_files:
        # Open TIFF file
        tiff_path = os.path.join(input_folder, tiff_file)
        with Image.open(tiff_path) as img:
            # Rotate by 90 degrees clockwise
            rotated_img = img.rotate(-90, expand=True)
            # Save as PNG with the same file name in the output folder
            png_path = os.path.join(output_folder, os.path.splitext(tiff_file)[0] + '.png')
            rotated_img.save(png_path, 'PNG')

if __name__ == "__main__":
    input_folder ="/media/diwakar/Data/Downloads/2013-01-10_lb3/2013-01-10/lb3/Cam5/"# input("Enter the path to the folder containing TIFF files: ")
    output_folder ="/media/diwakar/Data/Downloads/2013-01-10_lb3/2013-01-10/lb3/Cam5_png/" #input("Enter the path to the output folder for PNG files: ")

    tiff_to_png_and_rotate(input_folder, output_folder)
    print("Conversion and rotation complete.")








