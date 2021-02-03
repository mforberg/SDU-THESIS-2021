import grpc
import time
import minecraft_pb2_grpc
from variables import *
import multiprocessing
from multiprocessing import Pool

options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)


class Main:
    work = []

    def run(self):
        self.create_area_for_work()
        print(multiprocessing.cpu_count())
        first_time = time.time()
        result = self.pool_handler()
        print(time.time() - first_time)
        total_dict = {}
        for dick in result:
            total_dict.update(dick)
        print(len(total_dict))
        self.build_surface(total_dict)

    def create_area_for_work(self):
        for x in range(box_x_min, box_x_max):
            self.work.append((x, [box_z_min, box_z_max]))

    def work_log(self, work_data):
        # result = self.smart_row_read(work_data[0], work_data[0], work_data[1][0], work_data[1][1])
        result = self.read_part_of_world(work_data[0], work_data[0], work_data[1][0], work_data[1][1])['surface_dict']
        return result

    def pool_handler(self):
        p = Pool(int(multiprocessing.cpu_count() / 2))
        result = p.map(self.work_log, self.work)
        return result

    def build_surface(self, block_dict):
        blocks = []
        for value in block_dict.values():
            block = value["block"]
            block.type = WOOL
            blocks.append(block)
        client.spawnBlocks(Blocks(blocks=blocks))

    def read_part_of_world(self, min_x, max_x, min_z, max_z, min_y=30, max_y=160):
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


if __name__ == '__main__':
    Main().run()

