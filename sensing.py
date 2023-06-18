#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
import csv

def plot_data(log):
    img=Image.new("RGBA",(800,480),"White")
    draw=ImageDraw.Draw(img)
    prev_x,prev_y=log[0][0],log[0][1]
    draw.ellipse([(prev_x-5,prev_y-5), (prev_x+5,prev_y+5)], fill='red', outline=None, width=4)
    for ax in log[1:]:
        prev_x,prev_y=prev_x+ax[0],prev_y+ax[1]
        draw.point((prev_x,prev_y),fill='blue')
        draw.ellipse([(prev_x-5,prev_y-5), (prev_x+5,prev_y+5)], fill='red', outline=None, width=4)
        if ax[-1]==1:
            draw.ellipse([(prev_x-10,prev_y-10), (prev_x+10,prev_y+10)], fill='blue', outline=None, width=4)
            
    display(img)

log=[]
with open("./plot-2.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        row=[int(val) for val in row]
        log.append(row)
print(log)
plot_data(log)