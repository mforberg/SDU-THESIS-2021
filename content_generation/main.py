import map_analysis
from variables.map_variables import *
from variables.ga_map_variables import *
from variables.ga_type_variables import *
from map_ga.map_main import AreasGA
from type_ga.type_main import TypesGA
import minecraft_pb2_grpc
import grpc
import time
import copy


class Main:

    def run(self):
        first_time = time.time()
        total_block_dict, total_surface_dict, district_areas = map_analysis.MapAnalysis().run()
        print(f"Map analysis - Time: {time.time() - first_time}")
        # reset = input("reset surface? y/N - type anything and it will reset, aka. put grass :))")
        # if reset:
        #     self.grass_surface(surface_dict=total_surface_dict)
        first_time = time.time()
        result = AreasGA().run(areas=district_areas)
        print(f"GA - Time: {time.time() - first_time}")
        # TypesGA().run(surface_dict=total_surface_dict, areas=result)
        for area in result.population:
            self.build_surface(surface_dict=total_surface_dict, list_of_x_z_coordinates=area.list_of_coordinates)
        rollback = input("reset surface? Y/n - type anything and it will not rollback")
        if not rollback:
            self.rollback(surface_dict=total_surface_dict)

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
        blocks = []
        for value in surface_dict.values():
            block = copy.deepcopy(value['block'])
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
            if block.type in FLUID_LIST:
                continue
            block.type = GRASS
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))


if __name__ == '__main__':
    Main().run()
