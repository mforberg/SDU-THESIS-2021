import minecraft_pb2_grpc
from minecraft_pb2 import *
import grpc
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

    def build_solution(self, result):
        pass
