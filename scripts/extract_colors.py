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

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox



with open("output.json", "r") as fin:
    images = json.load(fin)['results']
    
def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df
   
def extract_colors(images):
    output = []
    #for index, item in enumerate(images, start=0):
    file_path = images[0]['path']
    # colors, pixel_count = extcolors.extract_from_path(file_path, tolerance=3, limit=3)
    # ic(index, colors)

    colors_x = extcolors.extract_from_path(file_path, tolerance = 4, limit = 4)
    df_color= color_to_df(colors_x)
    ic(type(df_color))
    return df_color
        

def donut_chart():
    df_color = extract_colors(images)
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p*100/sum(list_precent),1)) +'%' for c, p in zip(list_color,
                                                                                list_precent)]
    fig, ax = plt.subplots(figsize=(90,90),dpi=10)
    wedges, text = ax.pie(list_precent,
                        labels= text_c,
                        labeldistance= 1.05,
                        colors = list_color,
                        textprops={'fontsize': 120, 'color':'black'}
                        )
    plt.setp(wedges, width=0.3)

    #create space in the center
    plt.setp(wedges, width=0.36)

    ax.set_aspect("equal")
    fig.set_facecolor('white')
    plt.show()        
    
def color_palette():
    df_color = extract_colors(images)
    list_color = list(df_color['c_code'])
    fig, ax = plt.subplots(figsize=(192,108),dpi=10)
    fig.set_facecolor('white')
    plt.savefig('bg.png')
    plt.close(fig)

    #create color palette
    bg = plt.imread('bg.png')
    fig = plt.figure(figsize=(90, 90), dpi = 10)
    ax = fig.add_subplot(1,1,1)

    x_posi, y_posi, y_posi2 = 320, 25, 25
    for c in list_color:
        if  list_color.index(c) <= 5:
            y_posi += 125
            rect = patches.Rectangle((x_posi, y_posi), 290, 115, facecolor = c)
            ax.add_patch(rect)
            ax.text(x = x_posi+360, y = y_posi+80, s = c, fontdict={'fontsize': 150})
        else:
            y_posi2 += 125
            rect = patches.Rectangle((x_posi + 800, y_posi2), 290, 115, facecolor = c)
            ax.add_artist(rect)
            ax.text(x = x_posi+1160, y = y_posi2+80, s = c, fontdict={'fontsize': 150})
            
    ax.axis('off')
    plt.imshow(bg)
    plt.tight_layout()
    
    
if __name__ == "__main__":
    color_palette()