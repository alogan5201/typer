#!/usr/bin/env python3

# GET TOP 10 MOVIES AND OUTPUT TO FILE:
#       python update.py --count 10 --output output.json

# GET TOP 250 AND OUTPUT TO FILE
#       python update.py --output output.json

# GET TOP 250 AND OUTPUT TO CONSOLE
#       python update.py

# PRINT USAGE
#       python update.py --help

from slugify import slugify
from mapbox import Geocoder
from imdb import Cinemagoer

from multiprocessing import Pool
import argparse
import json
import time

# TODO: move this to environment variable for security
GEOCODER_ACCESS_TOKEN = 'pk.eyJ1IjoibG9nYW41MjAxIiwiYSI6ImNrcTQybTFoZzE0aDQyeXM1aGNmYnR1MnoifQ.4kRWNfEH_Yao_mmdgrgjPA'

geocoder = Geocoder(access_token=GEOCODER_ACCESS_TOKEN)
client = Cinemagoer()

BLACKLIST = [ 'attribution', 'type', 'query' ]

def update(movie):
    global client 
    
    movie.detail = client.get_movie(movie.movieID,info=('locations','plot','main'))
    return movie

def position(location):
    global geocoder 

    response = geocoder.forward(location,limit=1)
    data = None

    if response.status_code == 200:
        data = response.json()
        data['request'] = location

        for field in BLACKLIST:
            del data[field]

    return data

def fetch(count: int):
    global client

    result = client.get_top250_movies()[:count]
    output = []

    with Pool() as pool:
        result = pool.map(update,result)

    for i, movie in enumerate(result):
        id = movie.movieID
        title = movie.get('title')
        plot = ' '.join(movie.detail.get('plot'))
        locs = movie.detail.get('locations')
        cover = movie.detail.get('full-size cover url')
        slug = slugify(f"{title.lower()} {id}")

        locations = []

        if locs:
            names = [ l.split('::')[0] for l in locs if l ]

            with Pool() as pool:
                locations = [ l for l in pool.map(position,names) if l ]

        output.append({
            "index": i + 1, 
            "id": id, 
            "slug": slug, 
            "title": title, 
            "plot": plot,
            "image": cover,
            "locations": locations
        })

    data = { "results": output }
    return data


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Fetch and analyze movie data from imdb')
    parser.add_argument('-c','--count', type=int, default=250, help='The number of movies to fetch [<=250]')
    parser.add_argument('-o','--output', type=str, default=None, help='The output file [console]')
    parser.add_argument('-t','--timed', help='Print elapsed time after run')

    args = parser.parse_args()

    count = args.count
    output = args.output
    timed = args.timed

    start = time.time()
    data = fetch(count)
    end = time.time()

    data = json.dumps(data, sort_keys=True, indent=4)
    
    if output:
        with open(output,'w') as f:
            f.write(data)
    else:
        print(data)

    if timed:
        print(f"elapsed: {end - start}")