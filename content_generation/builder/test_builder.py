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
        self.x_diff = BOX_X_MAX - BOX_X_MIN
        self.z_diff = BOX_Z_MAX - BOX_Z_MIN

    def build_flat_surface(self, type_of_block: int):
        blocks = []
        for x in range(BOX_X_MIN, BOX_X_MAX + 1):
            for z in range(BOX_Z_MIN, BOX_Z_MAX + 1):
                for y in range(70, 75):
                    random_block = Block()
                    random_block.position.y = y
                    random_block.position.x = x
                    random_block.position.z = z
                    random_block.type = type_of_block
                    blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    # def create_cuts(self):
    #     blocks = []
    #     for x in range(BOX_X_MIN, BOX_X_MAX):
    #         for z in range(BOX_Z_MIN, BOX_Z_MAX):
    #             for y in range(70, 75):
    #                 if x % 6 == 0 or z % 6 == 0:
    #                     if y >= 74:
    #                         random_block = Block()
    #                         random_block.position.y = y
    #                         random_block.position.x = x
    #                         random_block.position.z = z
    #                         random_block.type = AIR
    #                         blocks.append(random_block)
    #     self.client.spawnBlocks(Blocks(blocks=blocks))

    def create_big_areas(self):
        default = False
        blocks = []
        build_x = default
        for temp_x in range(0, self.x_diff + 1):
            build_z = default
            x = temp_x + BOX_X_MIN
            if temp_x % 10 == 0:
                build_x = not build_x
            for temp_z in range(0, self.z_diff + 1):
                if temp_z % 10 == 0:
                    build_z = not build_z
                z = temp_z + BOX_Z_MIN
                y = 74
                random_block = Block()
                if build_x or build_z:
                    random_block.type = BEDROCK
                else:
                    random_block.type = AIR
                random_block.position.y = y
                random_block.position.x = x
                random_block.position.z = z
                blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))

    def create_walls(self):
        first_count = 24
        first_passed_x = False

        after_count = 19
        blocks = []
        x_counter = 0
        for temp_x in range(0, self.x_diff + 1):
            x = temp_x + BOX_X_MIN
            if not first_passed_x:
                if x_counter == first_count:
                    build_x = True
                elif x_counter == first_count + 1:
                    build_x = True
                    first_passed_x = True
                    x_counter = 0
                else:
                    build_x = False
            else:
                if x_counter == after_count:
                    build_x = True
                elif x_counter == after_count + 1:
                    build_x = True
                    x_counter = 0
                else:
                    build_x = False
            x_counter += 1
            z_counter = 0
            first_passed_z = False
            for temp_z in range(0, self.z_diff + 1):
                z = temp_z + BOX_Z_MIN
                if not first_passed_z:
                    if z_counter == first_count:
                        build_z = True
                    elif z_counter == first_count + 1:
                        build_z = True
                        first_passed_z = True
                        z_counter = 0
                    else:
                        build_z = False
                else:
                    if z_counter == after_count:
                        build_z = True
                    elif z_counter == after_count + 1:
                        build_z = True
                        z_counter = 0
                    else:
                        build_z = False
                z_counter += 1
                for y in range(75, 80):
                    random_block = Block()
                    if build_x or build_z:
                        random_block.type = BEDROCK
                    else:
                        random_block.type = AIR
                    random_block.position.y = y
                    random_block.position.x = x
                    random_block.position.z = z
                    blocks.append(random_block)
        self.client.spawnBlocks(Blocks(blocks=blocks))
