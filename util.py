# import cv2
from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

import constants
# def read_image(filename):
#    return cv2.imread(filename)

COLORS = ["r", "b", "g"]

def readable_image(filename):
    return "JPG" in filename.upper() and ("IMG" in filename.upper() or "RON" in filename.upper())

def read_image(filename):
    im = io.imread(filename)
    im_resized = resize(im, constants.DEFAULT_IMAGE_SIZE)
    return im_resized

def plot_points(x_values, y_values, x_name="", y_name=""):
    plt.scatter(x_values, y_values)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.show()

def plot_hist(hist, bin_edges):
    width = 0.7 * (bin_edges[1] - bin_edges[0])
    center = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()


def plot_freqs(freq1, freq2):
    bins = np.linspace(0, 1.5, 50)
    plt.hist([freq1, freq2], bins, label=['freq1', 'freq2'])
    plt.legend(loc='upper right')
    plt.show()

def plot_classes(classes):
    for i1, c1 in enumerate(classes):
        for i2, c2 in enumerate(c1):
            x_values = [i1 for t in range(len(c2))]
            y_values = c2
            plt.scatter(x_values, y_values, color=COLORS[i2])

    # plot
    plt.xlabel("Distance")
    plt.show()
