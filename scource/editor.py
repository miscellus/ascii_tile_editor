from math import *
from tkinter import *
from tkinter import ttk

from chunkmap import Layered_Chunk_Map, Tile

Tile.define_template("wall_tile", Tile(rep=u"█", tag="wall", collision=True))
Tile.define_template("bush_tile", Tile(rep="░", tag="nature", collision=True))
Tile.define_template("stair_tile", Tile(rep=u"▼"))

world = Layered_Chunk_Map(starting_layer="forest")

world.active_layer[1, 1] = world.make_chunk(fill=Tile(rep="I"))

for radius in range(5, 40, 10):
    for angle in range(0, 360, 3):
        angle = radians(angle)
        x, y = map(round, (cos(angle)*radius, sin(angle)*radius))
        world.set_tile(x, y, Tile.bush_tile)

for level in range(-50, 50, 20):
    for x in range(-50, 50, 1):
        y = level + 3*sin(x*0.1)
        x, y = map(round, (x, y))
        world.set_tile(x, y, Tile.wall_tile)

world.set_named_coord("staircase_01", *world.set_tile(11, 11, Tile.stair_tile))
world.set_named_coord("staircase_01", world.active_layer_name, 13, 13)
world.set_tile_at_named_coord("staircase_01", Tile.empty_tile)

root = Tk()

canvas_frame = ttk.Frame(root)
canvas = Canvas(canvas_frame, background="gray")
options_book = ttk.Notebook(root, borderwidth=5)

root.grid()
canvas_frame.grid(row=0, column=0, sticky="news")
canvas.grid(row=0, column=0, sticky="news")
options_book.grid(row=0, column=1, sticky="news")

root.columnconfigure(0, weight=4)
root.columnconfigure(1, weight=1, minsize=200)
root.rowconfigure(0, weight=1)
canvas_frame.columnconfigure(0, weight=1)
canvas_frame.rowconfigure(0, weight=1)
options_book.rowconfigure(0, weight=1)

canvas_items = []
# canvas_items.append(canvas.create_rectangle())

root.mainloop()