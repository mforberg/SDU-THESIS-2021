import minecraft_pb2_grpc
from variables.map_variables import *
import grpc
import copy


class TestBuilder:
    def __init__(self):
        __options = [('grpc.max_send_message_length', 512 * 1024 * 1024),
                     ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        __channel = grpc.insecure_channel('localhost:5001', options=__options)
        self.client = minecraft_pb2_grpc.MinecraftServiceStub(__channel)

    def build_flat_surface(self, type_of_block: int):
        blocks = []
        for x in range(BOX_X_MIN, BOX_X_MAX):
            for z in range(BOX_Z_MIN, BOX_Z_MAX):
                for y in range(70, 75):
                    random_block = Block()
                    random_block.position.y = y
                    random_block.position.x = x
                    random_block.position.z = z
                    random_block.type = type_of_block
                    blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def create_cuts(self):
        blocks = []
        for x in range(BOX_X_MIN, BOX_X_MAX):
            for z in range(BOX_Z_MIN, BOX_Z_MAX):
                for y in range(70, 75):
                    if x % 6 == 0 or z % 6 == 0:
                        if y >= 74:
                            random_block = Block()
                            random_block.position.y = y
                            random_block.position.x = x
                            random_block.position.z = z
                            random_block.type = AIR
                            blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def create_big_areas(self):
        blocks = []
        x_flipped = False
        z_flipped = False
        for x in range(BOX_X_MIN, BOX_X_MAX):
            if x % 10 == 0:
                x_flipped = not x_flipped
            for z in range(BOX_Z_MIN, BOX_Z_MAX):
                if z % 10 == 0:
                    z_flipped = not z_flipped
                for y in range(70, 75):
                    if y >= 74:
                        random_block = Block()
                        if x_flipped or z_flipped:
                            random_block.type = BEDROCK
                        else:
                            random_block.type = AIR
                        random_block.position.y = y
                        random_block.position.x = x
                        random_block.position.z = z
                        blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))
