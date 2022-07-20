import colorgram
from icecream import ic
import os, glob
import json

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def extractColors(file, colorAmount=3):
    # Extract 6 colors from an image.
    
    colors = colorgram.extract(file, colorAmount)

    # colorgram.extract returns Color objects, which let you access
    # RGB, HSL, and what proportion of the image was that color.
    first_color = colors[0]
    rgb = first_color.rgb # e.g. (255, 151, 210)
    hsl = first_color.hsl # e.g. (230, 255, 203)
    # proportion  = first_color.proportion # e.g. 0.34

    # # RGB and HSL are named tuples, so values can be accessed as properties.
    # # These all work just as well:
    # red = rgb[0]
    # red = rgb.r
    # saturation = hsl[1]
    # saturation = hsl.s
    ic(len(colors))

    # hex1=rgb_to_hex((colors[0].rgb[0], colors[0].rgb[1], colors[0].rgb[2]))
    # hex2=rgb_to_hex((colors[1].rgb[0], colors[1].rgb[1], colors[1].rgb[2]))
    # hex3=rgb_to_hex((colors[2].rgb[0], colors[2].rgb[1], colors[2].rgb[2]))
    #ic(colors[0].rgb, colors[1].rgb, colors[2].rgb)
    #ic(hex1, hex2, hex3)
    #output = {file: file, hex1: hex1, hex2: hex2, hex3: hex3}
    #ic(hex1, hex2, hex3)
    
    return colors
    
    
def extract_all(path):
    output = []
    for filename in glob.iglob(path + '**/*.png', recursive=True):
      #ic(filename)
        ic(filename)
        data = extractColors(filename, 3)
        output.append(data)
    return output
        

""" if __name__=='__main__':
    dir_path='/media/a/EXTERNAL-SS/downloads/snazzy-maps/popular/light/white/'
    #data  = extract_all(dir_path)
    #data = json.dumps(data, sort_keys=True, indent=4)
    with open("output.json", "r") as fin:
        images = json.load(fin)['results']
        output = []
        for index, item in enumerate(images[1:11], start=0):
            file_path = item['path']
            ic(item)
            colors = extractColors(file_path, 3)
            output.append(colors)
        ic(output) """

#extractColors('/media/a/EXTERNAL-SS/downloads/snazzy-maps/popular/light/white/229-simple-and-light.png', 3)

data = extractColors('/media/a/EXTERNAL-SS/downloads/snazzy-maps/popular/light/white/102-clean-grey.png', 3)


ic(data)