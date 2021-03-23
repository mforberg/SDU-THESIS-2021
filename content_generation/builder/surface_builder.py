import minecraft_pb2_grpc
from variables.map_variables import *
import grpc
import copy
from shared_variables import SolutionGA
from variables.wfc_variables import Tile


class SurfaceBuilder:

    anti_glass_blocks = []
    anti_trash_blocks = []
    anti_emerald_block = []

    def __init__(self):
        __options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                     ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        __channel = grpc.insecure_channel('localhost:5001', options=__options)
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(__channel)

    def build_type_ga(self, surface_dict: dict, type_ga_result: SolutionGA):
        list_of_building_blocks = {"Fishing": DIAMOND_ORE, "Trade": COAL_ORE, "Royal": GOLD_BLOCK, "Farms": OBSIDIAN,
                                   "Crafts": ICE, "Village": WOOL}
        blocks = []
        for district in type_ga_result.population:
            current_building_block = list_of_building_blocks[district.type_of_district]
            for coordinate in district.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])].block)
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def build_wfc_glass_layer(self, surface_dict: dict, wfc_tiles: List[Tile]):

        blocks = []
        for tile in wfc_tiles:
            current_building_block = GLASS
            for coordinate in tile.nodes:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])].block)
                block.position.y += 1
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))
        for block in blocks:
            block.type = AIR
        self.anti_glass_blocks = blocks

    def build_wfc_poop_layer(self, surface_dict: dict, wfc_tiles: List[Tile]):

        blocks = []
        for tile in wfc_tiles:
            current_building_block = EMERALD_BLOCK
            for coordinate in tile.nodes:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])].block)
                block.position.y += 2
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))
        for block in blocks:
            block.type = AIR
        self.anti_emerald_blocks = blocks

    def delete_wfc_poop_layer(self):
        self.client.spawnBlocks(Blocks(blocks=self.anti_emerald_blocks))

    def delete_wfc_glass_layer(self):
        self.client.spawnBlocks(Blocks(blocks=self.anti_glass_blocks))

    def build_wfc_trash_layer(self, surface_dict: dict, wfc_tiles: List[Tile]):
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK, DIAMOND_BLOCK]
        blocks = []
        counter = 0
        for tile in wfc_tiles:
            if counter >= len(list_of_building_blocks):
                counter = 0
            current_building_block = list_of_building_blocks[counter]
            for coordinate in tile.nodes:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])].block)
                block.position.y += 1
                block.type = current_building_block
                blocks.append(block)
            counter += 1
        self.client.spawnBlocks(Blocks(blocks=blocks))
        for block in blocks:
            block.type = AIR
        self.anti_trash_blocks = blocks

    def delete_wfc_trash_layer(self):
        self.client.spawnBlocks(Blocks(blocks=self.anti_trash_blocks))

    def build_clusters(self, surface_dict: dict, clusters: SolutionGA):
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK]
        blocks = []
        for cluster in clusters.population:
            current_building_block = list_of_building_blocks.pop(0)
            for value in cluster.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(value[0], value[1])].block)
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def rollback(self, surface_dict):
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK]
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value.block)
            if block.type == SPONGE:
                block.type = AIR
            if block.type in list_of_building_blocks:
                block.type = GRASS
            blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def build_from_list_of_tuples(self, surface_dict: dict, coordinates: List[tuple]):
        blocks = []
        for value in coordinates:
            block = copy.deepcopy(surface_dict[(value[0], value[1])].block)
            block.type = COBBLESTONE
            blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def grass_surface(self, surface_dict: dict):
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value.block)
            if block.type in FLUID_SET:
                continue
            block.type = GRASS
            blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))
