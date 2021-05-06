from typing import List

import minecraft_pb2_grpc
from minecraft_pb2 import *
import grpc
from wfc_models import Tile


class WFCBuilder:

    def __init__(self):
        __options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                     ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        __channel = grpc.insecure_channel('localhost:5001', options=__options)
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(__channel)
        self.dict_of_building_blocks = {"Fishing": DIAMOND_ORE, "Trade": RED_GLAZED_TERRACOTTA, "Royal": GOLD_BLOCK,
                                        "Farms": OBSIDIAN, "Crafts": ICE, "Village": WOOL}
        self.corner_builds = ['corner_upper_left', 'corner_upper_right', 'corner_bottom_left', 'corner_bottom_right']
        self.dot_builds = ['dot_upper_left', 'dot_upper_right', 'dot_bottom_left', 'dot_bottom_right']
        self.wall_builds = ['wall_left', 'wall_right', 'wall_upper', 'wall_bottom']

    def build_collapsed_tiles(self, surface_dict: dict, list_of_collapsed_tiles: List[Tile]):
        blocks = []
        for tile in list_of_collapsed_tiles:
            district_type = tile.district_type
            x, z = self.__get_smallest(tile=tile)
            y = surface_dict[(x, z)].y
            tile_type = tile.states[0].type
            print(tile_type)
            if tile_type in self.corner_builds or tile_type in self.wall_builds or tile_type == "floor":
                blocks.extend(self.__build_interior(x=x, z=z, y=y, district_type=district_type,
                                                    tile_type=tile_type, size=3))
            elif tile_type in self.dot_builds:
                blocks.extend(self.__build_exterior(x=x, z=z, y=y, district_type=district_type,
                                                    tile_type=tile_type, size=3))
            elif tile_type == "road":
                blocks.extend(self.__build_road(x=x, z=z, y=y, size=3))
            else:
                print(f"couldn't find type: {tile_type}")
        self.client.spawnBlocks(Blocks(blocks=blocks))
        input("3")
        input("2")
        input("1")
        for block in blocks:
            block.type = AIR
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def __build_interior(self, x: int, z: int, y: int, district_type: str, tile_type: str,
                         size: int) -> List[Block]:
        if tile_type == "corner_upper_left":
            x_value_for_wall = 0
            z_value_for_wall = size-1
        elif tile_type == "corner_upper_right":
            x_value_for_wall = size-1
            z_value_for_wall = size-1
        elif tile_type == "corner_bottom_left":
            x_value_for_wall = 0
            z_value_for_wall = 0
        elif tile_type == "corner_bottom_right":
            x_value_for_wall = size-1
            z_value_for_wall = 0
        elif tile_type == "wall_left":
            x_value_for_wall = 0
            z_value_for_wall = -1
        elif tile_type == "wall_right":
            x_value_for_wall = size-1
            z_value_for_wall = -1
        elif tile_type == "wall_upper":
            x_value_for_wall = -1
            z_value_for_wall = size-1
        elif tile_type == "wall_bottom":
            x_value_for_wall = -1
            z_value_for_wall = 0
        else:  # floor
            x_value_for_wall = -1
            z_value_for_wall = -1
        blocks = []
        for x_increase in range(0, size):
            if x_increase == x_value_for_wall:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, size):
                if z_increase == z_value_for_wall:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y_increase == 0:
                        floor = True
                    else:
                        floor = False
                    if y_increase == 3:
                        roof = True
                    else:
                        roof = False
                    random_block = Block()
                    random_block.position.x = x + x_increase
                    random_block.position.z = z + z_increase
                    random_block.position.y = y + y_increase
                    if floor:
                        random_block.type = PLANKS
                    elif roof:
                        random_block.type = self.dict_of_building_blocks[district_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __build_road(self, x: int, z: int, y: int, size: int) -> List[Block]:
        blocks = []
        for x_increase in range(0, size):
            for z_increase in range(0, size):
                random_block = Block()
                random_block.position.x = x + x_increase
                random_block.position.z = z + z_increase
                random_block.position.y = y
                random_block.type = GRASS_PATH
                blocks.append(random_block)
        return blocks

    def __build_exterior(self, x: int, z: int, y: int, district_type: str, tile_type: str,
                         size: int) -> List[Block]:
        if tile_type == "dot_upper_left":
            x_value_for_wall = 0
            z_value_for_wall = size - 1
        elif tile_type == "dot_upper_right":
            x_value_for_wall = size - 1
            z_value_for_wall = size - 1
        elif tile_type == "dot_bottom_left":
            x_value_for_wall = 0
            z_value_for_wall = 0
        elif tile_type == "dot_bottom_right":
            x_value_for_wall = size - 1
            z_value_for_wall = 0
        else:
            x_value_for_wall = 0
            z_value_for_wall = 0
            print("something wrong in build_exterior!")
        blocks = []
        for x_increase in range(0, size):
            if x_increase == x_value_for_wall:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, size):
                if z_increase == z_value_for_wall:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y_increase == 0:
                        continue
                    else:
                        random_block = Block()
                        random_block.position.x = x + x_increase
                        random_block.position.z = z + z_increase
                        random_block.position.y = y + y_increase
                        if x_wall and z_wall:
                            random_block.type = self.dict_of_building_blocks[district_type]
                        else:
                            random_block.type = AIR
                        blocks.append(random_block)
        return blocks

    def __get_smallest(self, tile: Tile) -> tuple:
        smallest = tile.nodes[0]
        for node in tile.nodes:
            if node < smallest:
                smallest = node
        return smallest
