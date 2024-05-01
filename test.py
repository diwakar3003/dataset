#!/usr/bin/python3
#
# Example code to read a velodyne_sync/[utime].bin file
# Plots the point cloud using matplotlib. Also converts
# to a CSV if desired. Saves the point cloud as a PLY file.
#
# To call:
#
#   python3 read_vel_sync.py velodyne.bin [out.csv] [out.ply]
#

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

def main(args):

    if len(sys.argv) < 2:
        print('Please specify velodyne file')
        return 1

    with open(sys.argv[1], "rb") as f_bin:
        if len(sys.argv) >= 3:
            print('Writing to ', sys.argv[2])
            with open(sys.argv[2], "w") as f_csv:
                hits = read_bin(f_bin, f_csv)
        else:
            hits = read_bin(f_bin)

    hits = np.array(hits)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(hits[:, 0], hits[:, 1], -hits[:, 2], c=-hits[:, 2], s=5, linewidths=0)
    plt.show()

    if len(sys.argv) >= 4:
        save_ply(hits, sys.argv[3])

    return 0

def read_bin(f_bin, f_csv=None):
    hits = []
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

        s = "%5.3f, %5.3f, %5.3f, %d, %d" % (x, y, z, i, l)

        if f_csv:
            f_csv.write('{}\n'.format(s))

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

if __name__ == '__main__':
    sys.exit(main(sys.argv))
