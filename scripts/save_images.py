
import os
import requests
from bs4 import BeautifulSoup
import cv2
from skimage import io
import colorgram
from icecream import ic
import argparse


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
#pages=1, sort="popular", tag="simple", color="white"
def save_image( pages:int, sort:str, tag:str, color:str):
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
    dir_path = f"Downloads/{sort}/{tag}/{color}/"
    file_path = f"Downloads/{sort}/{tag}/{color}/{sort}{tag}{color}.csv"

    create_dir(dir_path)
    create_file(file_path)

    f = open(file_path, "a")

    for tag in soup.find_all("span", class_="preview-image"):
        
        if tag.img:
            try:
                src = tag.img["src"]
                image = io.imread(src)
                name = src.split("/")[-1].split("?")[0]
                data = f"{name}\n"
                f.write(data)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imwrite(dir_path + name, image)
                print(name)
            except Exception as e:
                pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch images from snazzymaps')
    parser.add_argument('-p','--pages', type=int, default=1, help='Category; relevance, popular, recent')
    parser.add_argument('-s','--sort', type=str, default="popular", help='Category; relevance, popular, recent')
    parser.add_argument('-t','--tag', type=str, default="light", help='The Tag filter; light, simple, dark')
    parser.add_argument('-c','--color', type=str, default="white", help='Color; black, white, multi')
    
    args = parser.parse_args()

    pages = args.pages
    sort = args.sort
    tag = args.tag
    color = args.color



    
    max_pages = [1,2,3,4,5,6,7,8,9,10]
    # completed= psw;  psb;
    # plw
    for p in max_pages:
        save_image(pages, sort, tag, color )
    #save_image(term, pages=2)