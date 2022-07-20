# -*- coding: utf-8 -*-
import sys
from urllib.request import urlopen
import io
from icecream import ic
from colorthief import ColorThief
import json




with open("output.json", "r") as fin:
    images = json.load(fin)['results']


        
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def extract_colors():
    output = []
    for index, item in enumerate(images, start=0):
        item_path = item['src']
        fd = urlopen(item_path)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        palette = color_thief.get_palette(color_count=3)
        #print(color_thief.get_color(quality=1))
        #ic(color_thief.get_palette(quality=1))
        hex_values=[]
        for i in palette:
            hex= rgb_to_hex(i)
            hex_values.append(hex)

        ic(hex_values)
        
            






color_thief = ColorThief('/home/a/Workspace/typer/scripts/102-clean-grey.png')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=3)
first_color = palette[0]
#ic(first_color[0])


if __name__=='__main__':
    extract_colors()