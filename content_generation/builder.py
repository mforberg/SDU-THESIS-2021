from minecraft_pb2 import *
import minecraft_pb2_grpc
import grpc


class Builder:

    def __init__(self):
        self.options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
        self.channel = grpc.insecure_channel('localhost:5001', options=self.options)
        self.client = client = minecraft_pb2_grpc.MinecraftServiceStub(self.channel)
    
    def fill_cube(self, x_min:int, y_min:int, z_min:int, x_max:int, y_max, z_max:int, type:int = 5):
        self.client.fillCube(FillCubeRequest(  # Clear a 20x10x20 working area
            cube=Cube(
                min=Point(x=x_min, y=y_min, z=z_min),
                max=Point(x=x_max, y=y_max, z=z_max)
            ),
            type=type
        ))

    def draw_block(self, x:int, y:int, z:int, type:int = 41, orientation:int = 0):
        self.client.spawnBlocks(Blocks(Block(position=Point(x=x,y=y, z=z), type=type, orientation=orientation )))

    def draw_blocks_from_block_list(self, list_of_blocks:list) -> Blocks:
        self.client.spawnBlocks(Blocks(blocks=list_of_blocks))

    def draw_blocks_from_coordinate_list(self, list_of_coordinates:list, type:int = 41, orientation:int = 0):
        block_list = []
        for element in list:
            pass

    def batch_draw(self) -> None:
        pass
