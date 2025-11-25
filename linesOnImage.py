# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 22:52:58 2023

@author: CHJ2LIZ
"""

from PIL import Image, ImageDraw

im = Image.open('C:/Users/chj2liz/Pictures/cuphead3.png')

draw = ImageDraw.Draw(im)

for x in range(34):
    draw.line((x*75, 0, x*75, 2000), fill=50)
    
for y in range(40):
    draw.line((0, y*75, 1620, y*75), fill=50)
        
    
im.show()