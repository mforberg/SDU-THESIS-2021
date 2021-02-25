import minecraft_pb2_grpc
import multiprocessing
from multiprocessing import Pool
import time
import grpc
from map_variables import *
from ga_map_variables import *
import tqdm


options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
channel = grpc.insecure_channel('localhost:5001', options=options)
client = minecraft_pb2_grpc.MinecraftServiceStub(channel)


class MapAnalysis:
    work = []

    def run(self) -> [dict, dict, SolutionMap]:
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
        return total_block_dict, total_surface_dict, result

    def create_area_for_work(self):
        for x in range(BOX_X_MIN, BOX_X_MAX + 1):
            self.work.append({"x": x, "z_min": BOX_Z_MIN, "z_max": BOX_Z_MAX})

    def work_log(self, work_data):
        result = self.read_part_of_world(work_data["x"], work_data["x"], work_data["z_min"], work_data["z_max"])
        return result

    def pool_handler(self):
        p = Pool(int(multiprocessing.cpu_count() - 1))
        result = []
        for i in tqdm.tqdm(p.imap_unordered(self.work_log, self.work), total=len(self.work)):
            result.append(i)
        return result

    def read_part_of_world(self, min_x: int, max_x: int, min_z: int, max_z: int, min_y=30, max_y=160) -> [dict, dict]:
        cube_result = client.readCube(Cube(
            min=Point(x=min_x, y=min_y, z=min_z),
            max=Point(x=max_x, y=max_y, z=max_z)
        ))

        surface_dict = {}  # x z -> type y block
        block_dict = {}  # x y z -> type

        # changes the class structure to dictionaries + finds the surface
        for block in cube_result.blocks:
            x, y, z = block.position.x, block.position.y, block.position.z
            # block_dict[x, y, z] = {"type": block.type}
            if block.type not in SKIP_LIST:
                if (x, z) not in surface_dict:
                    surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
                elif surface_dict[x, z]["y"] < y:
                    surface_dict[x, z] = {"y": y, "type": block.type, "block": block}
        return {'surface_dict': surface_dict, 'block_dict': block_dict}

    def find_areas_for_districts(self, surface_dict: dict) -> SolutionMap:
        solution = SolutionMap(population=[], fitness=0)
        surface_dict_iter = iter(surface_dict)

        checked_nodes = set()
        start = time.time()
        while len(checked_nodes) < len(surface_dict):
            node = next(surface_dict_iter)
            if node not in checked_nodes:
                area = self.find_area(surface_dict, node[0], node[1], checked_nodes)
                if len(area.list_of_coordinates) >= MIN_SIZE_OF_AREA:
                    solution.population.append(area)
        print(f"End of while time: {time.time() - start}")
        print(f"Length of checked nodes {len(checked_nodes)}")
        return solution

    def find_area(self, surface_dict: dict, block_x: int, block_z: int, checked_nodes: Set[tuple]) -> AreaMap:
        nodes_to_be_checked = []
        min_x = block_x
        max_x = block_x
        min_z = block_z
        max_z = block_z
        total_x = block_x
        total_z = block_z
        amount = 1
        height = surface_dict[block_x, block_z]['y']
        checked_neighbors = []
        current_area = []
        current_area_set = set()
        nodes_to_be_checked.append((block_x, block_z))
        while nodes_to_be_checked:
            current_node = nodes_to_be_checked.pop()
            x = current_node[0]
            z = current_node[1]
            if surface_dict[current_node]['type'] not in FLUID_LIST:
                current_area.append(current_node)
                current_area_set.add(current_node)
                neighbors = self.get_neighbors(surface_dict, x, z)
                for neighbor in neighbors:
                    if neighbor not in checked_nodes and neighbor not in checked_neighbors \
                            and surface_dict[current_node]['y'] == surface_dict[neighbor]['y']:
                        checked_neighbors.append(neighbor)
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
            checked_nodes.add(current_node)
        mass_x = total_x / amount
        mass_z = total_z / amount
        return AreaMap(area_type="None", mass_coordinate={'x': mass_x, 'z': mass_z}, height=height,
                       area_set=current_area_set, coordinates=current_area,
                       min_max_values={"min_x": min_x, "max_x": max_x, "min_z": min_z, "max_z": max_z})

    def get_neighbors(self, surface_dict: dict, block_x: int, block_z: int) -> List[tuple]:
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
