import map_analysis
from variables.map_variables import *
from variables.shared_variables import *
from k_means.k_means_clustering import KMeansClustering
from map_ga.map_main import AreasGA
from type_ga.type_main import TypesGA
from wfc.preprocessing.wfc_preprocessing import WFCPreprocessing as WFC_PP
from builder.wfc_builder import WFCBuilder as WFCB
import minecraft_pb2_grpc
import grpc
import time
import copy


class Main:
    global_dict_of_used_coordinates = {}
    global_dict_of_types = {}

    def run(self):
        first_time = time.time()
        total_block_dict, total_surface_dict, district_areas, set_of_fluids = map_analysis.MapAnalysis().run()
        print(f"Map analysis - Time: {time.time() - first_time}")
        # reset = input("reset surface? y/N - type anything and it will reset, aka. put grass :))")
        # if reset:
        #     self.grass_surface(surface_dict=total_surface_dict)
        first_time = time.time()
        result = AreasGA().run(areas=district_areas)
        print(f"GA - Time: {time.time() - first_time}")

        for area in result.population:
            print(f"list of areas from first GA: {area.list_of_coordinates}")

        clusters = KMeansClustering().run(first_ga_result=result)
        for cluster in clusters.population:
            print(f"cluster contains: {len(cluster.list_of_coordinates)} blocks")

        self.build_clusters(clusters=clusters, surface_dict=total_surface_dict)
        rollback = input("reset surface? Y/n - type anything and it will not rollback")
        print("continued")
        if not rollback:
            self.rollback(surface_dict=total_surface_dict)

        first = time.time()
        result = TypesGA().run(surface_dict=total_surface_dict, clusters=clusters,
                               global_district_types_dict=self.global_dict_of_types, fluid_set=set_of_fluids)
        print(f"TYPE GA: {time.time()-first}")

        self.build_type_ga(surface_dict=total_surface_dict, type_ga_result=result)
        rollback = input("reset surface? Y/n - type anything and it will not rollback")
        print("continued")
        if not rollback:
            self.rollback(surface_dict=total_surface_dict)


        # WFC Start
        print("- - - - WFC RELATED GARBAGE KEEP SCROLLING - - - -")
        result = WFC_PP().create_tiles(result=result, tile_size=2)
        WFCB().build_tiles(surface_dict=total_surface_dict, tiles=result)
        print("- - - - WFC RELATED GARBAGE STOPPED - - - -")
        # WFC End

    def build_type_ga(self, surface_dict: dict, type_ga_result: SolutionGA):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        # ["Fishing", "Trade", "Royal", "Farms", "Crafts", "Village"]
        list_of_building_blocks = {"Fishing": DIAMOND_ORE, "Trade": COAL_ORE, "Royal": GOLD_BLOCK, "Farms": OBSIDIAN,
                                   "Crafts": ICE, "Village": WOOL}
        blocks = []
        for district in type_ga_result.population:
            print(district.type_of_district)
            current_building_block = list_of_building_blocks[district.type_of_district]
            for coordinate in district.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(coordinate[0], coordinate[1])]['block'])
                block.type = current_building_block
                blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))

    def build_clusters(self, surface_dict: dict, clusters: SolutionGA):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        list_of_building_blocks = [DIAMOND_ORE, COAL_ORE, GOLD_BLOCK, OBSIDIAN, ICE, NETHER_BRICK, SANDSTONE, WOOL,
                                   FURNACE, EMERALD_BLOCK]
        blocks = []
        for cluster in clusters.population:
            current_building_block = list_of_building_blocks.pop(0)
            for value in cluster.list_of_coordinates:
                block = copy.deepcopy(surface_dict[(value[0], value[1])]['block'])
                block.type = current_building_block
                blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))

    def build_surface(self, surface_dict, list_of_x_z_coordinates):
        print(list_of_x_z_coordinates)
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        blocks = []
        for value in list_of_x_z_coordinates:
            block = copy.deepcopy(surface_dict[value]['block'])
            block.type = DIAMOND_ORE
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))

    def rollback(self, surface_dict):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
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
        client.spawnBlocks(Blocks(blocks=blocks))

    def grass_surface(self, surface_dict: dict):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value['block'])
            if block.type in FLUID_SET:
                continue
            block.type = GRASS
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))


if __name__ == '__main__':
    Main().run()
