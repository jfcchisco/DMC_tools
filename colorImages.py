# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 14:51:56 2025

@author: CHJ2LIZ
"""

import json
import math
import pathlib

from PIL import Image, ImageDraw
from tkinter import filedialog


class stitchObj:
    def __init__(self, x, y, code):
        self.x = x
        self.y = y
        self.code = code


def parseJson(jsonFile):
    with open(jsonFile) as f:
        d = json.load(f)
    print('Loaded:', jsonFile)
    return d


def fileToStitches(objStr, width, height):
    s2return = []
    stitches = objStr['stitches'].split(',')
    lastID = 0
    for stitch in stitches:
        currID = int(stitch.split('-')[0])
        currCode = stitch.split('-')[1]
        while(lastID <= currID):
            x = lastID % width
            y = math.floor(lastID / width)
            s2return.append(stitchObj(x, y, currCode))
            lastID += 1
    return s2return


def main():
    global stitchesList, width, height
    
    jsonFile = parseJson(pathlib.Path
                         (filedialog.askopenfilename()))
    print(jsonFile['colors'])

    SIZE = 5
    width = int(jsonFile['properties']['width'])
    height = int(jsonFile['properties']['height'])
    imageW = width * SIZE
    imageH = height * SIZE

    stitchesList = fileToStitches(jsonFile, width, height)

    for color in jsonFile['colors']:
        print(color)
        out = Image.new(mode="RGB", size=(imageW, imageH))
        rect = ImageDraw.Draw(out)
        oneStitchFound = False
        blackCount = 0
        whiteCount = 0
        for stitch in stitchesList:
            x = stitch.x
            y = stitch.y
            shape = [(x * SIZE, y * SIZE), ((x + 1) * SIZE, (y + 1) * SIZE)]

            if(stitch.code == color['dmcCode']):
                oneStitchFound = True
                blackCount += 1
                rect.rectangle(shape, fill='black')
            else:
                whiteCount += 1
                rect.rectangle(shape, fill='white')
        if(oneStitchFound):
            percentage = int(blackCount * 10000 / (whiteCount + blackCount))
            out = out.save(f"out/{percentage:04d}_{color['dmcCode']}.png", 'PNG')

        # out.show()
    return 0


if __name__ == '__main__':
    main()
