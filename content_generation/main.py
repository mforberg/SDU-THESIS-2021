import map_analysis
from variables.map_variables import *
from map_ga.map_main import AreasGA
import minecraft_pb2_grpc
import grpc
import time


class Main:

    def run(self):
        first_time = time.time()
        total_block_dict, total_surface_dict, district_areas = map_analysis.MapAnalysis().run()
        print(f"Map analysis - Time: {time.time() - first_time}")
        self.reset_surface(surface_dict=total_surface_dict)
        first_time = time.time()
        result = AreasGA().run(total_block_dict=total_block_dict, total_surface_dict=total_surface_dict,
                               areas=district_areas)
        print(f"GA - Time: {time.time() - first_time}")
        print(len(result['population']))
        for area in result['population']:
            self.build_surface(surface_dict=total_surface_dict, list_of_x_z_coordinates=area['area'])

    def build_surface(self, surface_dict, list_of_x_z_coordinates):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        blocks = []
        for value in list_of_x_z_coordinates:
            block = surface_dict[value]['block']
            block.type = DIAMOND_ORE
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))

    def reset_surface(self, surface_dict: dict):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)
        blocks = []
        for value in surface_dict.values():
            block = value['block']
            if block.type in FLUID_LIST:
                continue
            block.type = GRASS
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))



if __name__ == '__main__':
    Main().run()
