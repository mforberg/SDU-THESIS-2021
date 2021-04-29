from typing import Set

import minecraft_pb2_grpc
import multiprocessing
from multiprocessing import Pool
import time
import grpc
from map_variables import *
import tqdm


options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)


class MapAnalysis:
    work = []
    possible_neighbor_relations = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def run(self) -> MapAnalData:
        total_surface_dict = {}
        total_block_dict = {}
        self.create_area_for_work()
        first_time = time.time()
        result = self.pool_handler()
        print("Time:", time.time() - first_time)
        for dictionary in result:
            total_block_dict.update(dictionary['block_dict'])
            total_surface_dict.update(dictionary['surface_dict'])
        result = self.find_areas_for_districts(total_surface_dict)
        map_anal_data = MapAnalData(surface_dict=total_surface_dict, block_dict=total_block_dict,
                                    set_of_fluid_coordinates=result[1], areas_for_districts=result[0])
        return map_anal_data

    def create_area_for_work(self):
        for x in range(BOX_X_MIN, BOX_X_MAX + 1):
            self.work.append({"x": x, "z_min": BOX_Z_MIN, "z_max": BOX_Z_MAX})

    def work_log(self, work_data):
        result = self.read_part_of_world(work_data["x"], work_data["x"], work_data["z_min"], work_data["z_max"], False)
        return result

    def pool_handler(self):
        p = Pool(int(multiprocessing.cpu_count() - 1))
        result = []
        for i in tqdm.tqdm(p.imap_unordered(self.work_log, self.work), total=len(self.work)):
            result.append(i)
        return result

    def read_part_of_world(self, min_x: int, max_x: int, min_z: int, max_z: int, block_dt: bool, min_y=30, max_y=160) -> dict:
        cube_result = client.readCube(Cube(
            min=Point(x=min_x, y=min_y, z=min_z),
            max=Point(x=max_x, y=max_y, z=max_z)
        ))

        surface_dict = {}  # x z -> type y block
        block_dict = {}  # x y z -> type

        # changes the class structure to dictionaries + finds the surface
        for block in cube_result.blocks:
            x, y, z = block.position.x, block.position.y, block.position.z
            if block_dt:
                block_dict[x, y, z] = {"type": block.type, "block": block}
            if block.type not in SKIP_SET:
                if (x, z) not in surface_dict:
                    surface_dict[x, z] = SurfaceDictionaryValue(y=y, block_type=block.type, block=block)
                elif surface_dict[x, z].y < y:
                    surface_dict[x, z] = SurfaceDictionaryValue(y=y, block_type=block.type, block=block)
        return {'surface_dict': surface_dict, 'block_dict': block_dict}

    def find_areas_for_districts(self, surface_dict: dict) -> (SolutionGA, set):
        solution = SolutionGA(population=[], fitness=0)
        fluid_blocks_set = set()
        checked_nodes = set()
        start = time.time()
        for node in surface_dict:
            if node not in checked_nodes:
                area = self.find_area(surface_dict, node[0], node[1], checked_nodes, fluid_blocks_set)
                if len(area.list_of_coordinates) >= MIN_SIZE_OF_AREA:
                    solution.population.append(area)
        print(f"End of while time: {time.time() - start}")
        print(f"Length of checked nodes {len(checked_nodes)}")
        return solution, fluid_blocks_set

    def find_area(self, surface_dict: dict, block_x: int, block_z: int, checked_nodes: Set[tuple],
                  fluid_blocks_set: set) -> SolutionArea:
        nodes_to_be_checked = []
        min_x = max_x = total_x = block_x
        min_z = max_z = total_z = block_z
        amount = 1
        height = surface_dict[block_x, block_z].y
        checked_neighbors = set()
        current_area = []
        nodes_to_be_checked.append((block_x, block_z))
        while nodes_to_be_checked:
            current_node = nodes_to_be_checked.pop()
            x = current_node[0]
            z = current_node[1]
            if surface_dict[current_node].block_type not in FLUID_SET:
                current_area.append(current_node)
                neighbors = self.get_neighbors(surface_dict, x, z)
                for neighbor in neighbors:
                    if neighbor not in checked_nodes and neighbor not in checked_neighbors \
                            and surface_dict[current_node].y == surface_dict[neighbor].y:
                        checked_neighbors.add(neighbor)
                        nodes_to_be_checked.append(neighbor)
                        amount += 1
                total_x += x
                total_z += z
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
                if z > max_z:
                    max_z = z
                if z < min_z:
                    min_z = z
            else:
                fluid_blocks_set.add((x, z))
            checked_nodes.add(current_node)
        mass_x = total_x / amount
        mass_z = total_z / amount
        return SolutionArea(mass_coordinate={'x': mass_x, 'z': mass_z}, height=height, coordinates=current_area,
                            min_max_values={"min_x": min_x, "max_x": max_x, "min_z": min_z, "max_z": max_z},
                            type_of_district="no")

    def get_neighbors(self, surface_dict: dict, block_x: int, block_z: int) -> List[tuple]:
        neighbors = []  # [[x1, z1], [x2, z2]]
        for possible_neighbor_relation in self.possible_neighbor_relations:
            possible_neighbor = (possible_neighbor_relation[0] + block_x, possible_neighbor_relation[1] + block_z)
            if possible_neighbor in surface_dict:
                neighbors.append(possible_neighbor)
        return neighbors
