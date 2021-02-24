from typing import List
import random


class TypeFitness:

    def calculate_fitness_for_all(self, populations: List[List[dict]]):
        for solution in populations:
            self.calculate_individual_fitness(solution=solution)

    def calculate_individual_fitness(self, solution: List[dict]):
        # solution['fitness'] = random.randint(0, 10000)
        pass
