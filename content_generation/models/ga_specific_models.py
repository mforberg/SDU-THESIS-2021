import copy
import csv
from os import path
from typing import List

from shared_models import SolutionGA


class DataFileCreator:

    def __init__(self, filename: str):
        self.folder = "stats/"
        i = 1
        new_file_name = filename
        while path.exists(f"{self.folder}{new_file_name}.csv"):
            new_file_name = filename + str(i)
            i += 1
        self.filename = new_file_name

    def check_stats_on_solution(self, population: List[SolutionGA], current_gen: int, best_solution: SolutionGA):
        new_best_prints = []
        min_fitness = 99999999999999
        max_fitness = -1
        avg_fitness = 0
        for solution in population:
            fitness = solution.fitness
            avg_fitness += fitness
            if fitness < min_fitness:
                min_fitness = fitness
            elif fitness > max_fitness:
                max_fitness = fitness
                if fitness > best_solution.fitness:
                    best_solution = copy.deepcopy(solution)
                    new_best_prints.append(f"New best {solution.fitness} at gen {current_gen}")
        data = {'Min': min_fitness, 'Max': max_fitness, 'Avg': avg_fitness / len(population)}
        # self.__store_stats(gen=current_gen, data=data)
        return new_best_prints, best_solution

    def __store_stats(self, gen: int, data: dict):
        with open(f"{self.folder}{self.filename}.csv", "a", newline='') as file:
            fieldnames = ['Generation', 'Min_fitness', 'Max_fitness', 'Avg_fitness']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow({'Generation': gen, 'Min_fitness': data['Min'], 'Max_fitness': data['Max'],
                             'Avg_fitness': data['Avg']})