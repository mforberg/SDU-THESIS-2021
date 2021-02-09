import minecraft_pb2_grpc
import multiprocessing
from multiprocessing import Pool
import time
import grpc
from variables import *


options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)


class MapAnalysis:
    work = []

    def run(self):
        total_surface_dict = {}
        total_block_dict = {}
        self.create_area_for_work()
        first_time = time.time()
        result = self.pool_handler()
        print("Time:", time.time() - first_time)
        for dictionary in result:
            total_block_dict.update(dictionary['block_dict'])
            total_surface_dict.update(dictionary['surface_dict'])
        district_areas = self.find_areas_for_districts2(total_surface_dict)
        district_areas.sort(key=len, reverse=True)
        return total_block_dict, total_surface_dict, district_areas

    def create_area_for_work(self):
        for x in range(box_x_min, box_x_max + 1):
            self.work.append({"x": x, "z_min": box_z_min, "z_max": box_z_max})

    def work_log(self, work_data):
        result = self.read_part_of_world(work_data["x"], work_data["x"], work_data["z_min"], work_data["z_max"])
        return result

    def pool_handler(self):
        p = Pool(int(multiprocessing.cpu_count() / 2))
        result = p.map(self.work_log, self.work)
        return result

    def read_part_of_world(self, min_x, max_x, min_z, max_z, min_y=30, max_y=160):
        cube_result = client.readCube(Cube(
            min=Point(x=min_x, y=min_y, z=min_z),
            max=Point(x=max_x, y=max_y, z=max_z)
        ))

        surface_dict = {}  # x z -> type y block
        block_dict = {}  # x y z -> type

        # changes the class structure to dictionaries + finds the surface
        for block in cube_result.blocks:
            x, y, z = block.position.x, block.position.y, block.position.z
            block_dict[x, y, z] = {"type": block.type}
            if block.type not in skip_list:
                if (x, z) not in surface_dict:
                    surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
                elif surface_dict[x, z]["y"] < y:
                    surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
        return {"surface_dict": surface_dict, "block_dict": block_dict}

    # def find_areas_for_districts(self, surface_dict):
    #     areas = []
    #     checked_nodes = []
    #     nodes_to_be_checked = []
    #     current_area = []
    #     for block in surface_dict:
    #         nodes_to_be_checked.append(block)
    #         current_area.append(block)
    #         break
    #     while nodes_to_be_checked:
    #         current_node = nodes_to_be_checked.pop()
    #         checked_nodes.append(current_node)
    #         neighbors = self.get_neighbors(surface_dict, current_node[0], current_node[1])
    #         for neighbor in neighbors:
    #             nodes_to_be_checked.append(neighbor)
    #             if surface_dict[current_node]['y'] == surface_dict[neighbor]['y']:
    #                 current_area.append(neighbor)
    #     return areas

    def find_areas_for_districts2(self, surface_dict):
        areas = []
        surface_dict_iter = iter(surface_dict)
        checked_nodes = []
        while len(checked_nodes) < len(surface_dict):
            cheese = next(surface_dict_iter)
            if cheese not in checked_nodes:
                result = self.fill_me_daddy(surface_dict, cheese[0], cheese[1], checked_nodes)
                areas.append(result)
        return areas

    def fill_me_daddy(self, surface_dict, block_x, block_z, checked_nodes):
        nodes_to_be_checked = []
        checked_neighbors = []
        current_area = []
        nodes_to_be_checked.append((block_x, block_z))
        while nodes_to_be_checked:
            current_node = nodes_to_be_checked.pop()
            x = current_node[0]
            z = current_node[1]
            current_area.append(current_node)
            neighbors = self.get_neighbors(surface_dict, x, z)
            for neighbor in neighbors:
                if neighbor not in checked_nodes and neighbor not in checked_neighbors \
                        and surface_dict[current_node]['y'] == surface_dict[neighbor]['y']:
                    checked_neighbors.append(neighbor)
                    current_area.append(neighbor)
                    nodes_to_be_checked.append(neighbor)
            checked_nodes.append(current_node)
        return current_area

    def get_neighbors(self, surface_dict, block_x, block_z):
        neighbors = []  # [[x1, z1], [x2, z2]]
        for x in range(-1, 2):
            if x != 0:
                if (block_x + x, block_z) in surface_dict:
                    neighbors.append((block_x+x, block_z))
        for z in range(-1, 2):
            if z != 0:
                if (block_x, block_z + z) in surface_dict:
                    neighbors.append((block_x, block_z + z))
        return neighbors
