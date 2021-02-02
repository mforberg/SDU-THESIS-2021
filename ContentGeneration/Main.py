import grpc

import minecraft_pb2_grpc
from minecraft_pb2 import *

options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)


skip_list = [AIR, TALLGRASS, RED_FLOWER, YELLOW_FLOWER, LEAVES, VINE, SAPLING]  # List of blocks that is ignored


def read_part_of_word(min_x, max_x, min_z, max_z):
    result = client.readCube(Cube(
        min=Point(x=min_x, y=30, z=min_z),
        max=Point(x=max_x, y=200, z=max_z)
    ))

    surface_dict = {}  # x z -> type y
    block_dict = {}  # x y z -> type y

    # changes the class structure to dictionaries + finds the surface
    for block in result.blocks:
        if block.type not in skip_list:
            x, y, z = block.position.x, block.position.y, block.position.z
            block_dict[x, y, z] = block.type
            if (x, z) not in surface_dict:
                surface_dict[x, z] = y, block.type
            elif surface_dict[x, z][0] < y:
                surface_dict[x, z] = y, block.type
    return surface_dict, block_dict


class Main:
    total_surface_dict = {}  # x z -> type y
    total_block_dict = {}  # x y z -> type y

    def run(self):
        for i in range(1, 401, 40):
            sur_dict, block_dict = read_part_of_word(i, i+40, i, i+40)
            self.total_surface_dict.update(sur_dict)
            self.total_block_dict.update(block_dict)
        print(len(self.total_block_dict))


Main().run()

# client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
#     cube=Cube(
#         min=Point(x=-10, y=4, z=-10),
#         max=Point(x=10, y=14, z=10)
#     ),
#     type=AIR
# ))
# client.spawnBlocks(Blocks(blocks=[  # Spawn a flying machine
#     # Lower layer
#     Block(position=Point(x=2, y=5, z=1), type=PISTON, orientation=NORTH),
#     Block(position=Point(x=2, y=5, z=0), type=SLIME, orientation=NORTH),
#     Block(position=Point(x=2, y=5, z=-1), type=STICKY_PISTON, orientation=SOUTH),
#     Block(position=Point(x=2, y=5, z=-2), type=PISTON, orientation=NORTH),
#     Block(position=Point(x=2, y=5, z=-4), type=SLIME, orientation=NORTH),
#     # Upper layer
#     Block(position=Point(x=2, y=6, z=0), type=REDSTONE_BLOCK, orientation=NORTH),
#     Block(position=Point(x=2, y=6, z=-4), type=REDSTONE_BLOCK, orientation=NORTH),
#     # Activate
#     Block(position=Point(x=2, y=6, z=-1), type=QUARTZ_BLOCK, orientation=NORTH),
#     # TEST
#     Block(position=Point(x=1, y=4, z=1), type=GLOWSTONE, orientation=NORTH),
#     Block(position=Point(x=0, y=4, z=0), type=FARMLAND, orientation=NORTH),
#     Block(position=Point(x=0, y=5, z=0), type=WHEAT, orientation=NORTH),
#     Block(position=Point(x=1, y=4, z=0), type=WATER),
#     Block(position=Point(x=0, y=4, z=1), type=GRASS),
#     Block(position=Point(x=0, y=4, z=2), type=GRASS_PATH),
# ]))
