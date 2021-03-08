import minecraft_pb2_grpc
from variables.map_variables import *
import grpc
import copy
from shared_variables import SolutionGA


class WFCBuilder:

    def __init__(self):
        __options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        __channel = grpc.insecure_channel('localhost:5001', options=__options)
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(__channel)

    def build_tiles(self, surface_dict: dict, tiles: SolutionGA):
        """
        Builds N x N blocks on top of provided areas to illustrate how the tiles will be placed on the areas
        @param surface_dict: dictionary containing all blocks read from the map initially
        @param tiles: N x N squares returned by a method in wfc_preprocessing
        """
        blocks = []
        cube_result = self.client.readCube(Cube(
            min=Point(x=10, y=40, z=10),
            max=Point(x=20, y=50, z=20)
        ))
        print("DUMMY BUILD TILES")

    def build_type_ga(self, surface_dict: dict, type_ga_result: SolutionGA):
        list_of_building_blocks = {"Fishing": DIAMOND_ORE, "Trade": COAL_ORE, "Royal": GOLD_BLOCK, "Farms": OBSIDIAN,
                                   "Crafts": ICE, "Village": WOOL}
        blocks = []
        for district in type_ga_result.population:
            current_building_block = list_of_building_blocks[district.type_of_district]
            for coordinate in district.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])]['block'])
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def build_clusters(self, surface_dict: dict, clusters: SolutionGA):
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK]
        blocks = []
        for cluster in clusters.population:
            current_building_block = list_of_building_blocks.pop(0)
            for value in cluster.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(value[0], value[1])]['block'])
                block.type = current_building_block
                blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def rollback(self, surface_dict):
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK]
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value['block'])
            if block.type == SPONGE:
                block.type = AIR
            if block.type in list_of_building_blocks:
                block.type = GRASS
            blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def grass_surface(self, surface_dict: dict):
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value['block'])
            if block.type in FLUID_SET:
                continue
            block.type = GRASS
            blocks.append(block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def build_solution(self, result):
        pass
