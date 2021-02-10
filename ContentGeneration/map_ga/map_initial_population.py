from ..variables import *
import random


class InitialPopulation:

    def create(self):
        print("hello")

    def get_random_coordinate(self):
        x = random.randint(box_x_min, box_x_max)
        z = random.randint(box_z_min, box_z_max)
        return x, z
