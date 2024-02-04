import copy
import tkinter as tk
import random
from config import *
import time

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

root = tk.Tk()
# root.geometry(f"{WIDTH+250}x{HEIGHT+25}")
root.configure(background = BACKGROUNDCOLOR)

canvas_frame = tk.Frame(bg=BACKGROUNDCOLOR)

canvas = tk.Canvas(canvas_frame, width=WIDTH, height=HEIGHT, bg=BACKGROUNDCOLOR)
canvas.pack(anchor='nw')

yyy = 0
def oldxyset(rr):
    
    global line
    line[2] = rr.x
    line[3] = rr.y

canvas.bind("<ButtonPress-1>", oldxyset)


canvas_frame.grid(row=0, column=0)



diapason = 0


def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_rect(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_rectangle(x, y, x1, y1, outline=_from_rgb(color), width=5)

def draw_line(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_line(x, y, x1, y1, fill=_from_rgb(color), width=5)


def collision_lines(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2 # not 90 deg
    x = ((y3-y1)*(x2-x1)*(x4-x3) + x1*(y2-y1)*(x4-x3) - x3*(y4-y3)*(x2-x1)) / ((y2-y1)*(x4-x3) - (y4-y3)*(x2-x1))
    y = (x-x1)*(y2-y1)/(x2-x1)+y1
    if x3 <= x <= x4 and y3 <= y <= y4 and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
        return (x,y)

def all_collisions_line_rect(line, rect):
    points = []
    for x in range(2):
        point = collision_lines(line, [rect[0] if x == 0 else rect[2], rect[1], rect[0] if x == 0 else rect[2], rect[3]])
        if point:
            points += [point]
    for y in range(2):
        point = collision_lines(line, [rect[0], rect[1] if y == 0 else rect[3], rect[2], rect[1] if y == 0 else rect[3]])
        if point:
            points += [point]
    return points



rect = [254, 67, 337, 476]
line = [53, 235, 483, 356]

x1, y1, x2, y2 = line
x3, y3, x4, y4 = 254, 67, 254, 476


while True:
    draw_line(canvas, *line)
    draw_rect(canvas, *rect)
    for x,y in all_collisions_line_rect(line, rect):    
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=_from_rgb((100, 200, 100)))
    canvas.update()