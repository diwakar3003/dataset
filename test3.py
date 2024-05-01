import os
import cv2
import numpy as np
import pandas as pd

def lidar_to_image(lidar):
    """Convert a Lidar point cloud to a 2D bird's eye view image.

    :param lidar: Lidar point cloud Nx5 (x, y, z, intensity, ring)
    :type lidar: np.array
    :return: 2D bird's eye view image with the Lidar information
    :rtype: np.array
    """
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    height = image.shape[0]
    width = image.shape[1]

    # Normalize x and y coordinates
    x_normalized = ((lidar[:, 0] - np.min(lidar[:, 0])) / (np.max(lidar[:, 0]) - np.min(lidar[:, 0]))) * width
    y_normalized = ((lidar[:, 1] - np.min(lidar[:, 1])) / (np.max(lidar[:, 1]) - np.min(lidar[:, 1]))) * height

    # Convert intensity to color
    intensity_normalized = ((lidar[:, 3] - np.min(lidar[:, 3])) / (np.max(lidar[:, 3]) - np.min(lidar[:, 3]))) * 255

    # Draw Lidar points on the image
    for x, y, intensity in zip(x_normalized, y_normalized, intensity_normalized):
        cv2.circle(image, (int(x), int(y)), 1, (intensity, intensity, intensity), -1)

    return image

def read_lidar(lidar_path):
    """Read Lidar point cloud from a CSV file.

    :param lidar_path: Path to the Lidar CSV file
    :type lidar_path: str
    :return: Lidar point cloud Nx5 (x, y, z, intensity, ring)
    :rtype: np.array
    """
    return pd.read_csv(lidar_path, delimiter=',').values

def generate_bev_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for csv_file in os.listdir(input_folder):
        if csv_file.endswith('.csv'):
            csv_file_path = os.path.join(input_folder, csv_file)
            lidar = read_lidar(csv_file_path)
            lidar_bev = lidar_to_image(lidar)
            bev_image_path = os.path.join(output_folder, os.path.splitext(csv_file)[0] + '.png')
            cv2.imwrite(bev_image_path, lidar_bev)

if __name__ == '__main__':
    input_folder = '/media/diwakar/Data/Downloads/2013-01-10_vel/2013-01-10/lidar_csv/'#input("Enter the path to the folder containing .csv files: ")
    output_folder ='/media/diwakar/Data/Downloads/2013-01-10_vel/2013-01-10/lidar_bev/' #input("Enter the path to the output folder for BEV images: ")

    generate_bev_images(input_folder, output_folder)
