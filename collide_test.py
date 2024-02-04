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


canvas_frame.grid(row=0, column=0)


diapason = 0

def draw_net(canvas):
    for x in range(W):
        for y in range(H):
            canvas.create_rectangle(x * SIZE, y * SIZE, x * SIZE+SIZE, y * SIZE+SIZE, outline='grey')


def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_rect(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_rectangle(x, y, x1, y1, outline=_from_rgb(color), width=5)

def draw_line(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_line(x, y, x1, y1, fill=_from_rgb(color), width=5)


def collision_lines(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    x = ((y3-y1)*(x2-x1)*(x4-x3) + x1*(y2-y1)*(x4-x3) - x3*(y4-y3)*(x2-x1)) / ((y2-y1)*(x4-x3) - (y4-y3)*(x2-x1))
    y = (x-x1)*(y2-y1)/(x2-x1)+y1
    return (x,y)

def collision_line_rect(line, rect):
    points = []
    for x in range(2):
        points += [collision_lines(line, [rect[0] if x == 0 else rect[2], rect[1], rect[0] if x == 0 else rect[2], rect[3]])]
    # for y in range(2):
    #     points += [collision_lines(line, [rect[0], rect[1] if x == 0 else rect[3], rect[2], rect[3]])]
    return points



rect = [254, 67, 337, 476]
line = [53, 235, 483, 356]

x1, y1, x2, y2 = line
x3, y3, x4, y4 = 254, 67, 254, 476


while True:
    draw_line(canvas, *line)
    draw_rect(canvas, *rect)
    for x,y in collision_line_rect(line, rect):    
        canvas.create_oval(x-5, y-5, x+5, y+5, fill=_from_rgb((100, 200, 100)))
    canvas.update()