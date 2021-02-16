import map_analysis
from minecraft_pb2 import *
from map_ga import map_main
import minecraft_pb2_grpc
import grpc


class Main:

    def run(self):
        total_block_dict, total_surface_dict, district_areas = map_analysis.MapAnalysis().run()
        map_main.DistrictGA().run(total_block_dict=total_block_dict, total_surface_dict=total_surface_dict,
                                  district_areas=district_areas)
        # for i in range(0, 20):
        #     print(len(district_areas[i]))
        # self.build_surface(total_surface_dict, district_areas)

    # def build_surface(self):
    #     blocks = []
    #     for value in total_surface_dict.values():
    #         block = value["block"]
    #         block.type = PACKED_ICE
    #         blocks.append(block)
    #     client.spawnBlocks(Blocks(blocks=blocks))

    def build_surface(self, surface_dict, district_areas):
        options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                   ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:5001', options=options)
        client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

        biggest_surface = district_areas[0]

        blocks = []
        for value in biggest_surface:
            block = surface_dict[value]['block']
            block.type = REDSTONE_BLOCK
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))


if __name__ == '__main__':
    Main().run()
