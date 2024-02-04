import math
import tkinter as tk
from config import *
from collider import *

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
    
    global objects
    objects[0].x = rr.x
    objects[0].y = rr.y
    objects[0].cx, objects[0].cy = objects[0].x + SIZE//2, objects[0].y + SIZE//2

canvas.bind("<ButtonPress-1>", oldxyset)


canvas_frame.grid(row=0, column=0)

def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

def draw_rect(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_rectangle(x, y, x1, y1, outline=_from_rgb(color), width=5)

def draw_line(canvas, x, y, x1, y1, color=(200, 100, 100)):
    canvas.create_line(x, y, x1, y1, fill=_from_rgb(color), width=5)



objects = []
objects = [Agent(objects) for x in range(5)]



# line = [53, 235, 483, 356]


radius = 150
rays = 8
deg_betw_rays = 360 / rays



while True:
    
    for obj in objects:
        rect = [obj.x, obj.y, obj.x + SIZE, obj.y + SIZE]



        lines = []
        for r in range(rays):
            x1, y1 = obj.cx, obj.cy
            x2, y2 = 0, 0
            rads = math.radians(r*deg_betw_rays+0.1)
            x2 = x1 + radius*math.cos(rads)
            y2 = y1 + radius*math.sin(rads)
            lines += [[x1, y1, x2, y2]]


        for l in lines:
            draw_line(canvas, *l)
        draw_rect(canvas, *rect)   

        for oo in objects:
            if not oo is obj:
                points = []
                for line in lines:
                    pp = all_collisions_line_rect(line, [oo.x, oo.y, oo.x + SIZE, oo.y + SIZE])
                    if pp:
                        points += pp
                for x,y in points:    
                    canvas.create_oval(x-5, y-5, x+5, y+5, fill=_from_rgb((100, 200, 100))) 
        

    
    
    
    canvas.update()
    canvas.delete("all")