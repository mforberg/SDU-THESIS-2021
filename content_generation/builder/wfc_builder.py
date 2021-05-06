from typing import List

import minecraft_pb2_grpc
from minecraft_pb2 import *
import grpc
from shared_models import SurfaceDictionaryValue
from wfc_models import Tile


class WFCBuilder:

    def __init__(self):
        __options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                     ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        __channel = grpc.insecure_channel('localhost:5001', options=__options)
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(__channel)
        self.dict_of_building_blocks = {"Fishing": DIAMOND_ORE, "Trade": RED_GLAZED_TERRACOTTA, "Royal": GOLD_BLOCK,
                                        "Farms": OBSIDIAN, "Crafts": ICE, "Village": WOOL}

    def build_collapsed_tiles(self, surface_dict: dict, list_of_collapsed_tiles: List[Tile]):
        blocks = []
        for tile in list_of_collapsed_tiles:
            current_type = tile.type_of_tile
            x, z = tile.nodes[0]
            y = surface_dict[(x, z)].y
            tile_type = tile.states[0].type
            blocks_template = getattr(self, f'__get_blocks_{tile_type}')(x, z, y, current_type)

    def __get_blocks_corner_upper_left(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 0:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                if z == 2:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_corner_upper_right(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 2:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                if z == 2:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_corner_bottom_left(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 0:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                if z == 0:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_corner_bottom_right(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 2:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                if z == 0:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_wall_left(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 0:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_wall_right(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 2:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_wall_upper(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            for z_increase in range(0, 3):
                if z == 2:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_wall_bottom(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            for z_increase in range(0, 3):
                if z == 0:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_floor(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            for z_increase in range(0, 3):
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get_blocks_road(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            for z_increase in range(0, 3):
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    random_block = Block()
                    random_block.position.x = x + x_increase
                    random_block.position.z = z + z_increase
                    random_block.position.y = y + y_increase
                    if floor:
                        random_block.type = GRASS_PATH
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    def __get2_blocks_corner_upper_left(self, x, z, y, current_type) -> List[Block]:
        blocks = []
        for x_increase in range(0, 3):
            if x == 0:
                x_wall = True
            else:
                x_wall = False
            for z_increase in range(0, 3):
                if z == 2:
                    z_wall = True
                else:
                    z_wall = False
                for y_increase in range(0, 4):
                    if y == 0:
                        floor = True
                    else:
                        floor = False
                    if y == 3:
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
                        random_block.type = self.dict_of_building_blocks[current_type]
                    elif x_wall or z_wall:
                        random_block.type = COBBLESTONE
                    else:
                        random_block.type = AIR
                    blocks.append(random_block)
        return blocks

    # def build_tiles(self, surface_dict: dict, tiles: SolutionGA):
    #     """
    #     Builds N x N blocks on top of provided areas to illustrate how the tiles will be placed on the areas
    #     @param surface_dict: dictionary containing all blocks read from the map initially
    #     @param tiles: N x N squares returned by a method in wfc_preprocessing
    #     """
    #     blocks = []
    #     pass
