import grpc
import time
import minecraft_pb2_grpc
from minecraft_pb2 import *
import multiprocessing
from multiprocessing import Pool

options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)

# List of blocks that is ignored
skip_list = [AIR, TALLGRASS, RED_FLOWER, YELLOW_FLOWER, CHORUS_FLOWER, LEAVES, LEAVES2, VINE, SAPLING, WATERLILY,
             RED_MUSHROOM, BROWN_MUSHROOM, REEDS, POTATOES, MELON_BLOCK, MELON_STEM, PUMPKIN_STEM, PUMPKIN, DEADBUSH,
             SNOW_LAYER, WHEAT, RAIL, CHORUS_PLANT, DOUBLE_PLANT, FIRE, COCOA, CARROTS, CACTUS]


def read_part_of_world(min_x, max_x, min_z, max_z, min_y=30, max_y=160):
    cube_result = client.readCube(Cube(
        min=Point(x=min_x, y=min_y, z=min_z),
        max=Point(x=max_x, y=max_y, z=max_z)
    ))

    surface_dict = {}  # x z -> type y block
    block_dict = {}  # x y z -> type

    # changes the class structure to dictionaries + finds the surface
    for block in cube_result.blocks:
        if block.type not in skip_list:
            x, y, z = block.position.x, block.position.y, block.position.z
            block_dict[x, y, z] = {"type": block.type}
            if (x, z) not in surface_dict:
                surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
            elif surface_dict[x, z]["y"] < y:
                surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
    return {"surface_dict": surface_dict, "block_dict": block_dict}


# def read_block(x, z, y):
#     result = client.readCube(Cube(
#         min=Point(x=x, y=y, z=z),
#         max=Point(x=x, y=y, z=z)
#     ))
#
#     return result.blocks

# TODO: put stuff in main and upgrade surface search to be the same as the commented code
class Main:
    pass
    # total_surface_dict = {}  # x z -> type y block
    # total_block_dict = {}  # x y z -> type

    # def run(self):
    # sur_dict, block_dict = read_part_of_world(1, 50, 1, 50)
    # self.total_surface_dict.update(sur_dict)
    # self.total_block_dict.update(block_dict)
    # print(self.total_surface_dict)
    # self.pillar_read(1, 11, 1, 11)

    # def pillar_read(self, min_x, max_x, min_z, max_z):
    #     first_read = True
    #     row_y = 100
    #     last_y = 100
    #     for x in range(min_x, max_x):
    #         new_row = True
    #         for z in range(min_z, max_z):
    #             if first_read:
    #                 block = self.find_surface(x, z)
    #                 self.total_surface_dict[x, z] = {"y": block.position.y, "type": block.type, "block": block}
    #                 last_y = block.position.y
    #                 first_read = False
    #                 print("only once")
    #             else:
    #                 if new_row:
    #                     last_y = row_y
    #                     block = self.find_surface(x, z, last_y)
    #                     self.total_surface_dict[x, z] = {"y": block.position.y, "type": block.type, "block": block}
    #                     last_y = block.position.y
    #                     row_y = block.position.y
    #                     new_row = False
    #                     print("new row")
    #                 else:
    #                     block = self.find_surface(x, z, last_y)
    #                     self.total_surface_dict[x, z] = {"y": block.position.y, "type": block.type, "block": block}
    #                     last_y = block.position.y
    #                     print("spam")
    #     print(self.total_surface_dict)

    # def find_surface(self, x, z, y=160):
    #     counter = 0
    #     surface_found = False
    #     last_was_in_skip_list = False
    #     read_more_than_once = False
    #     old_block = None
    #     while not surface_found:
    #         counter += 1
    #         block = read_block(x, z, y)[0]
    #         if counter > 300:
    #             return -1
    #         elif block.type in skip_list:
    #             if not last_was_in_skip_list and read_more_than_once:
    #                 return old_block
    #             old_block = block
    #             y -= 1
    #             last_was_in_skip_list = True
    #             read_more_than_once = True
    #             continue
    #         else:
    #             if last_was_in_skip_list and read_more_than_once:
    #                 return block
    #             old_block = block
    #             y += 1
    #             last_was_in_skip_list = False
    #             read_more_than_once = True
    #             continue

    # def build_surface(self):
    #     blocks = []
    #     for value in self.total_surface_dict.values():
    #         block = value["block"]
    #         block.type = PACKED_ICE
    #         blocks.append(block)
    #     client.spawnBlocks(Blocks(blocks=blocks))


work = []


# TODO: Rename
def rly_smart():
    x_min = 1
    x_max = 201
    z_min = -201
    z_max = -1

    for x in range(x_min, x_max):
        work.append((x, [z_min, z_max]))


def work_log(work_data):
    result1 = read_part_of_world(work_data[0], work_data[0], work_data[1][0], work_data[1][1])['surface_dict']
    return result1


def pool_handler():
    p = Pool(int(multiprocessing.cpu_count() / 2))
    total_result = p.map(work_log, work)
    return total_result


def build_surface(dict2):
    blocks = []
    for value in dict2.values():
        block = value["block"]
        block.type = PACKED_ICE
        blocks.append(block)
    client.spawnBlocks(Blocks(blocks=blocks))


if __name__ == '__main__':
    rly_smart()
    print(multiprocessing.cpu_count())
    first_time = time.time()
    result = pool_handler()
    print(time.time() - first_time)
    total_dict = {}
    for dick in result:
        total_dict.update(dick)
    print(len(total_dict))
    build_surface(total_dict)

# print(work)

# Main().run()


# Main().build_surface()
