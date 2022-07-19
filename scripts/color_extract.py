import colorgram
from icecream import ic
import os, glob

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def extractColors(file, colorAmount):
    # Extract 6 colors from an image.
    colors = colorgram.extract(file, colorAmount)

    # colorgram.extract returns Color objects, which let you access
    # RGB, HSL, and what proportion of the image was that color.
    first_color = colors[0]
    rgb = first_color.rgb # e.g. (255, 151, 210)
    hsl = first_color.hsl # e.g. (230, 255, 203)
    proportion  = first_color.proportion # e.g. 0.34

    # RGB and HSL are named tuples, so values can be accessed as properties.
    # These all work just as well:
    red = rgb[0]
    red = rgb.r
    saturation = hsl[1]
    saturation = hsl.s


    hex1=rgb_to_hex((colors[0].rgb[0], colors[0].rgb[1], colors[0].rgb[2]))
    hex2=rgb_to_hex((colors[1].rgb[0], colors[1].rgb[1], colors[1].rgb[2]))
    hex3=rgb_to_hex((colors[2].rgb[0], colors[2].rgb[1], colors[2].rgb[2]))
    #ic(colors[0].rgb, colors[1].rgb, colors[2].rgb)

    ic(hex1, hex2, hex3)
    
    
    
root_dir='/home/a/Workspace/color-extract/'


for filename in glob.iglob(root_dir + '**/*.png', recursive=True):
      extractColors(filename, 3)