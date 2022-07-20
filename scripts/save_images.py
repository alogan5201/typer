# -*- coding: utf-8 -*-
import sys
from urllib.request import urlopen
import io
import os, glob
from numpy import extract
import requests
from bs4 import BeautifulSoup
import cv2
#from skimage import io
import colorgram
from icecream import ic
import argparse
import json
from colorthief import ColorThief
import requests

with open("../db.json", "r") as fin:
    db = json.load(fin)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def extract_colors(item_path):
    output = []
    
    # item_path = item['src']
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
    return hex_values
def create_dir(path):
    """ Create folders """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print("Error")

def create_file(path):
    """ Create a file """
    try:
        if not os.path.exists(path):
            f = open(path, "w")
            f.write("Name,Alt\n")
            f.close()
    except OSError:
        print("Error")
def write_post(query):
    
    data = db[query]
    last = data[-1]
    last_id = last['id']
    increment_id= last_id + 1
    ic(increment_id)
    post = {"id": increment_id, "title": "test", "author": "andrew"}
    url = f"http://localhost:3004/{query}"
    response = requests.post(url, json=post)
    x=response.json()
    #ic(data['id'])
    return x
#pages=1, sort="popular", tag="simple", color="white"
def save_image( pages:int, sort:str, tag:str, color:str, directory:str):
    ## URL and headers
    # https://snazzymaps.com/explore?page=1&sort=popular&tag=simple&color=white
    
    url = "https://snazzymaps.com/explore?page="+str(pages)+"&sort="+sort+"&tag="+tag+"&color="+color
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    ## making a GET request to the website and getting the information in response.
    result = requests.get(url, headers=header)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
    else:
        print("Error")
        exit()

    ## Paths and file for saving the images and data.
    dir_path = f"{directory}{sort}/{tag}/{color}/"
    file_path = f"{directory}{sort}/{tag}/{color}/{sort}{tag}{color}.csv"

    create_dir(dir_path)
    create_file(file_path)

    f = open(file_path, "a")
    output = []
    for tag in soup.find_all("span", class_="preview-image"):
        
        if tag.img:
            try:
                src = tag.img["src"]
                #image = io.imread(src)
                name = src.split("/")[-1].split("?")[0]
                data = f"{name}\n"
                #f.write(data)
                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                #cv2.imwrite(dir_path + name, image)
                #ic(src, image, data)
                
                file_name = dir_path + name
                hex_values = extract_colors(src)
                output.append({"name": name, "src": src, "path": file_name, "hex_values": hex_values})
            except Exception as e:
                pass
    
    
    data = { "palettes": output }
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch images from snazzymaps')
    parser.add_argument('-p','--pages', type=int, default=1, help='Category; relevance, popular, recent')
    parser.add_argument('-s','--sort', type=str, default="popular", help='Category; relevance, popular, recent')
    parser.add_argument('-t','--tag', type=str, default="light", help='The Tag filter; light, simple, dark')
    parser.add_argument('-c','--color', type=str, default="white", help='Color; black, white, multi')
    parser.add_argument('-o','--output', type=str, default=None, help='The output file [console]')
    parser.add_argument('-d','--directory', type=str, default="/media/a/EXTERNAL-SS/downloads/snazzy-maps/", help='The output directory for images [console]')

    args = parser.parse_args()

    pages = args.pages
    sort = args.sort
    tag = args.tag
    color = args.color
    output = args.output
    directory = args.directory
    data = save_image(pages, sort, tag, color, directory)
    
    data = json.dumps(data, sort_keys=True, indent=4)
    
    img_dir_path = f"{directory}{sort}/{tag}/{color}/"
    
    
    
 
    if output:
        with open(output,'w') as f:
            f.write(data)
    else:
        ic(data)


