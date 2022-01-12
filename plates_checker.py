#!/usr/bin/python
import json
import os

FILENAME_KNOWN_PLATES = 'known_plates.json'

def process_plates(plates_list: list):
    try:
        # Opening JSON file
        f = open(FILENAME_KNOWN_PLATES)

        # returns JSON object as
        # a dictionary
        known_plates = json.load(f)

        # Closing file
        f.close()
        print(plates_list)
        print(known_plates)

    except FileNotFoundError as e:
        with open(FILENAME_KNOWN_PLATES, 'w') as fp:
            json.dump({}, fp)
