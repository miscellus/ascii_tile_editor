from collections import defaultdict
from math import *
from pprint import pprint

class Tile:
    templates = []

    def __init__(self, rep, tag="generic", collision=False, poperties=None):
        self.rep = rep
        self.collision = collision
        self.tag = tag
        self.poperties = poperties

    @classmethod
    def define_template(cls, template_name, tile):
        cls.templates.append(tile)
        tile.template_index = len(cls.templates) - 1
        setattr(cls, template_name, tile)

Tile.define_template("null_tile", Tile(rep=u"·", tag="null"))
Tile.define_template("empty_tile", Tile(rep=" ", tag="empty"))
Tile.define_template("wall_tile", Tile(rep=u"█", tag="wall", collision=True))
Tile.define_template("bush_tile", Tile(rep="░", tag="nature", collision=True))
Tile.define_template("stair_tile", Tile(rep=u"▼"))

class Layered_Chunk_Map:
    """
    A Layered_Chunk_Map stores layeres of tile maps, seperated into chunks.
    Because the tile data is stored in chunks, one does not need to store 
    data in-between defined areas of the map, making a sparse world better optimized.

    Notes on specification:
        self.chunks (dict) maps layer_names (strings) to layers which are dictionaries
        mapping chunk-coordinates (2-tuples)
        to chunks (two-dimensional lists of tiles with dimensions: chunk_width, chunk_height)

        self.named_coords (dict) maps world coordinate names (strings) to 
        3-tuples of format: (layer_name, world_x, world_y)
    """

    def __init__(self, starting_layer="start", chunk_width=8, chunk_height=8):

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        self.chunks = {}
        self.named_coords = {}
        
        self.active_layer = None
        self.active_layer_name = ""

        self.define_layer(starting_layer, set_as_active=True)

    def define_layer(self, layer_name, set_as_active=False):
        if layer_name not in self.chunks:
            self.chunks[layer_name] = defaultdict(self.make_chunk)
            if set_as_active:
                self.switch_layer(layer_name)
        else:
            raise DuplicateKeyError(layer_name)

    def switch_layer(self, layer_name):
        self.active_layer = self.chunks[layer_name]
        self.active_layer_name = layer_name

    def split_full_coordinate(self, x, y):
        chunk_x, local_x = divmod(x, self.chunk_width)
        chunk_y, local_y = divmod(y, self.chunk_height)
        chunk_index = (chunk_x, chunk_y)

        return (chunk_index, local_x, local_y)

    def make_chunk(self, fill=Tile.empty_tile):
        return [[fill for i in range(self.chunk_width)] for j in range(self.chunk_height)]

    def get_tile(self, x, y):
        chunk_index, local_x, local_y = self.split_full_coordinate(x, y)

        if chunk_index in self.active_layer:
            tile = self.active_layer[chunk_index][local_y][local_x]
        else:
            tile = Tile.null_tile

        return tile

    def set_tile(self, x, y, tile):
        chunk_index, local_x, local_y = self.split_full_coordinate(x, y)

        self.active_layer[chunk_index][local_y][local_x] = tile

        return (self.active_layer_name, x, y)

    def set_named_coord(self, name, layer_and_coord):
        self.named_coords[name] = layer_and_coord

    def set_tile_at_named_coord(self, coord_name, tile):
        layer, x, y = self.named_coords[coord_name]
        self.switch_layer(layer)
        self.set_tile(x, y, tile)

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

world.set_named_coord("staircase_01", world.set_tile(11, 11, Tile.stair_tile))
world.set_named_coord("staircase_01", (world.active_layer_name, 13, 13))
world.set_tile_at_named_coord("staircase_01", Tile.empty_tile)

for j in range(-50,50):
    for i in range(-50, 50):
        print(world.get_tile(i, j).rep, end="")
    print()