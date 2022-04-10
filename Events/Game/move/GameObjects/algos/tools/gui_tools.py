from tkinter import Canvas

from Events.Game.move.GameObjects.algos.tools.point import Point


def create_circle(x,y, r, canvas, color): #center coordinates, radius

    x0 =x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1,fill=color,outline=color)

def create_squer(x, y, x1, y1, canvas:Canvas):
    canvas.create_rectangle(x, y, x1, y1, fill="blue")

def transfer_point_to_gui_format(point:Point,map_size):
    new_position=Point(0,0)
    new_position.x=point.x+map_size/2.0
    new_position.y=point.y-map_size/2.0
    return new_position

def create_line(start:Point,end:Point,canvas:Canvas,color):
    canvas.create_line(start.x,start.y,end.x,end.y,fill=color,width=2)


