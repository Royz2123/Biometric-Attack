import cv2


def read_image(filename):
    return cv2.imread(filename)

def plot_points(x_values, y_values, x_name="", y_name=""):
    plt.scatter(x_values, y_values)
    plt.ylabel(y_name)
    plt.xlabel(x_name)
    plt.show()
