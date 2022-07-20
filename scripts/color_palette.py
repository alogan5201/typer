import cv2
import extcolors
from colormap import rgb2hex
import json
from icecream import ic

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

import PIL
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



with open("output.json", "r") as fin:
    images = json.load(fin)['results']
    

   
def extract_colors(images):
    output = []
    for index, item in enumerate(images, start=0):
        file_path = item['path']
        img = PIL.Image.open(file_path)
        colors, pixel_count = extcolors.extract_from_image(img, image=f"output/{item['name']}")
        
        
        
        
if __name__ == "__main__":
    extract_colors(images)
    