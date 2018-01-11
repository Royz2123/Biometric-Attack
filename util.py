# import cv2
from skimage import io
import matplotlib.pyplot as plt

# def read_image(filename):
#    return cv2.imread(filename)

def readable_image(filename):
    return "JPG" in filename.upper() and ("IMG" in filename.upper() or "RON" in filename.upper())

def read_image(filename):
    return io.imread(filename)

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


def plot_classes(class1, class2):
    plt.scatter(class1, [0 for i in range(len(class1))], color="r")
    plt.scatter(class2, [0 for i in range(len(class2))], color="b")
    plt.xlabel("Distance")
    plt.show()
