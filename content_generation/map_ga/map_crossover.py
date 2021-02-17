import random
import copy
from variables.ga_map_variables import *


class MapCrossover:
    parent_list = []

    def crossover(self, population_dict, parent_list):
        self.parent_list = parent_list
        new_population = []
        ordered_population_dict = copy.deepcopy(population_dict)
        ordered_population_dict.sort(key=lambda x: x['fitness'], reverse=True)
        # pick top x
        for i in ordered_population_dict:
            new_population.append(i['population'])
            if i == ELITISM_AMOUNT:
                break
        while len(new_population) > POPULATION_SIZE:
            parents = self.find_two_parents()
            result = self.create_offspring(parents['p1'], parents['p2'])
            new_population.append(result['c1'])
            if len(new_population) > POPULATION_SIZE:
                new_population.append(result['c2'])
        return new_population

    def find_two_parents(self):
        parent1 = self.get_parent()
        parent2 = self.get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def get_parent(self):
        random_index = random.randint(0, len(self.parent_list) - 1)
        return self.parent_list[random_index]

    def create_offspring(self, parent1, parent2):
        random.shuffle(parent1)
        random.shuffle(parent2)
        if len(parent1) > len(parent2):
            return self.single_point_crossover(shortest=parent2, longest=parent1)
        else:
            return self.single_point_crossover(shortest=parent1, longest=parent2)

    def single_point_crossover(self, shortest, longest):
        point = random.randint(0, len(shortest)-1)
        child1 = []
        child2 = []
        flip = False
        for i in range(0, len(longest)):
            if i == point:
                flip = True
            if not flip:
                if i < len(shortest) - 1:
                    child1.append(shortest[i])
                child2.append(longest)
            else:
                if i < len(shortest) - 1:
                    child2.append(shortest[i])
                child1.append(longest[i])
        return {"c1": child1, "c2": child2}
