from collections import defaultdict
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

Tile.define_template("null_tile", Tile(rep="·", tag="null"))
Tile.define_template("empty_tile", Tile(rep=" ", tag="empty"))

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

    def set_named_coord(self, name, layer, x, y):
        self.named_coords[name] = layer, x, y

    def set_tile_at_named_coord(self, coord_name, tile):
        layer, x, y = self.named_coords[coord_name]
        self.switch_layer(layer)
        self.set_tile(x, y, tile)