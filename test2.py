import os
import sys
import struct
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def convert(x_s, y_s, z_s):
    scaling = 0.005  # 5 mm
    offset = -100.0
    x = x_s * scaling + offset
    y = y_s * scaling + offset
    z = z_s * scaling + offset
    return x, y, z

def read_bin_file(bin_file_path, csv_file_path=None):
    hits = []
    with open(bin_file_path, "rb") as f_bin:
        if csv_file_path:
            with open(csv_file_path, "w") as f_csv:
                while True:
                    x_str = f_bin.read(2)
                    if not x_str:  # eof
                        break
                    x = struct.unpack('<H', x_str)[0]
                    y = struct.unpack('<H', f_bin.read(2))[0]
                    z = struct.unpack('<H', f_bin.read(2))[0]
                    i = struct.unpack('B', f_bin.read(1))[0]
                    l = struct.unpack('B', f_bin.read(1))[0]
                    x, y, z = convert(x, y, z)
                    s = "%5.3f, %5.3f, %5.3f, %d, %d\n" % (x, y, z, i, l)
                    f_csv.write(s)
                    hits.append([x, y, z])
        else:
            while True:
                x_str = f_bin.read(2)
                if not x_str:  # eof
                    break
                x = struct.unpack('<H', x_str)[0]
                y = struct.unpack('<H', f_bin.read(2))[0]
                z = struct.unpack('<H', f_bin.read(2))[0]
                i = struct.unpack('B', f_bin.read(1))[0]
                l = struct.unpack('B', f_bin.read(1))[0]
                x, y, z = convert(x, y, z)
                hits.append([x, y, z])
    return hits

def save_ply(points, filename):
    with open(filename, 'w') as f:
        num_points = len(points)
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(num_points))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("end_header\n")
        for point in points:
            f.write("{} {} {}\n".format(point[0], point[1], point[2]))

def main(input_folder, output_csv_folder, output_ply_folder):
    if not os.path.isdir(input_folder):
        print("Input folder doesn't exist.")
        return 1
    for bin_file in os.listdir(input_folder):
        if bin_file.endswith('.bin'):
            bin_file_path = os.path.join(input_folder, bin_file)
            # csv_folder = os.path.join(output_csv_folder, os.path.splitext(bin_file)[0])
            # ply_folder = os.path.join(output_ply_folder, os.path.splitext(bin_file)[0])
            # os.makedirs(csv_folder, exist_ok=True)
            # os.makedirs(ply_folder, exist_ok=True)
            csv_file_path = os.path.join(output_csv_folder, os.path.splitext(bin_file)[0] + '.csv')
            ply_file_path = os.path.join(output_ply_folder, os.path.splitext(bin_file)[0] + '.ply')
            print('Processing:', bin_file_path)
            hits = read_bin_file(bin_file_path, csv_file_path)
            hits = np.array(hits)
            # fig = plt.figure()
            # ax = fig.add_subplot(111, projection='3d')
            # ax.scatter(hits[:, 0], hits[:, 1], -hits[:, 2], c=-hits[:, 2], s=5, linewidths=0)
            # plt.show()
            save_ply(hits, ply_file_path)

if __name__ == '__main__':
    # if len(sys.argv) < 4:
    #     print('Usage: python3 script.py input_folder output_csv_folder output_ply_folder')
    #     sys.exit(1)
    input_folder ='/media/diwakar/Data/Downloads/2013-01-10_vel/2013-01-10/velodyne_sync/' #sys.argv[1]
    output_csv_folder = '/media/diwakar/Data/Downloads/2013-01-10_vel/2013-01-10/lidar_csv/'#sys.argv[2]
    output_ply_folder ='/media/diwakar/Data/Downloads/2013-01-10_vel/2013-01-10/lidar_ply/' #sys.argv[3]
    main(input_folder, output_csv_folder, output_ply_folder)
