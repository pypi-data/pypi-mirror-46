import os
import re
import numpy as np
import pytesseract
from skimage import io


def convert_dir(dir_path):
    """
    Convert all the images in a directory to text
    -----------
    Parameters:
    dir_path: string representing the path to the directory
    Return:
    list with strings representing the text on the images inside the directory
    """
    imgs = []
    for img in os.listdir(dir_path):
        if re.search('\.png$', img):
            imgs.append(os.path.join(dir_path, img))

    return [convert_img(img_path) for img_path in imgs]


def convert_img(img_path):
    """
    Convert to text of an image to a string
    -----------
    Parameters:
    img_path: string representing the path to the img
    return:
    string representing the text in the image
    """
    img = load_img(img_path)
    return pytesseract.image_to_string(img, lang='eng')


def load_img(img_path):
    """
    Load an img and assert the pixel values are in the
    0-255 range
    -----------
    Parameters:
    img_path: string representing the path to the img
    Return:
    numpy array with the loaded image
    """
    img = io.imread(img_path)

    if np.amax(img) <= 1:
        raise('Something is wrong with the image pixel values,'
              ' talk to Heitor to find out whats the problem')
    return img
