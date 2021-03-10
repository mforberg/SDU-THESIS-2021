import random
import multiprocessing
from multiprocessing import Pool
from variables.ga_map_variables import *
from variables.shared_variables import *
from .map_fitness import MapFitness
from thread_thingy import ThisIsThreadThing
from concurrent.futures import as_completed, wait


work = []
thing = ThisIsThreadThing()


def k_point_crossover(k: int, shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
    points = set()
    while len(shortest) > len(points) and k >= len(points):
        new_value = False
        while not new_value:
            point = random.randint(0, len(shortest)-1)
            if point not in points:
                new_value = True
                points.add(point)
    child1 = []
    child2 = []
    flip = False
    for i in range(0, len(longest)):
        if i in points:
            flip = not flip
        if not flip:
            if i < len(shortest):
                child1.append(shortest[i])
            child2.append(longest[i])
        else:
            if i < len(shortest):
                child2.append(shortest[i])
            child1.append(longest[i])
    return {"c1": child1, "c2": child2}


def uniform_crossover(shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
    child1 = []
    child2 = []
    for i in range(0, len(longest)):
        if random.randint(0, 1) == 0:
            if i < len(shortest):
                child1.append(shortest[i])
            child2.append(longest[i])
        else:
            if i < len(shortest):
                child2.append(shortest[i])
            child1.append(longest[i])
    return {"c1": child1, "c2": child2}


def dynamic_application_of_operators(shortest: List[SolutionArea], longest: List[SolutionArea]) -> dict:
    __create_work(shortest=shortest, longest=longest)
    best_crossover_result = {"fitness": 0, 'children': {'c1': None, 'c2': None}}
    result = pool_handler()
    for dictionary in result:
        if dictionary['fitness'] > best_crossover_result['fitness']:
            best_crossover_result = dictionary
    return best_crossover_result['children']


def work_log(work_data):
    print("hello")
    index = work_data['index']
    if index == 0:
        result = uniform_crossover(shortest=work_data['shortest'], longest=work_data['longest'])
    else:
        result = k_point_crossover(shortest=work_data['shortest'], longest=work_data['longest'], k=index)
    fitness1 = MapFitness().calculate_fitness_from_population(population=result['c1'])
    fitness2 = MapFitness().calculate_fitness_from_population(population=result['c2'])
    return {"fitness": fitness1 + fitness2, "children": result}


def pool_handler():
    result = []
    # p = Pool(int(multiprocessing.cpu_count() - 1))
    # result1 = self.thing.submit(self.work_log, self.work)
    future_list = []
    future = thing.executor.submit(work_log, work)
    future_list.append(future)
    print("0")
    for x in as_completed(future_list):
        try:
            print(x.result())
        except:
            print("olol")
    return result


def __create_work(shortest: List[SolutionArea], longest: List[SolutionArea]):

    for i in range(0, MAX_AREAS_IN_CITY):
        work.append({"shortest": copy.deepcopy(shortest), "longest": copy.deepcopy(longest), "index": i})


class MapCrossover:

    def __init__(self):
        self.parent_list = []
        self.work = []

    def crossover(self, population_list: List[SolutionGA], parent_list: List[List[SolutionArea]]) -> List[SolutionGA]:
        self.parent_list = parent_list
        new_population = []
        ordered_population_list = population_list
        ordered_population_list.sort(key=lambda x: x.fitness, reverse=True)
        # pick top x
        i = 0
        for solution in ordered_population_list:
            if i == MAP_ELITISM_AMOUNT:
                break
            i += 1
            new_population.append(copy.deepcopy(solution))
        while len(new_population) < MAP_POPULATION_SIZE:
            parents = self.__find_two_parents()
            result = self.create_offspring(parents['p1'], parents['p2'])
            new_population.append(SolutionGA(fitness=0, population=result['c1']))
            if len(new_population) < MAP_POPULATION_SIZE:
                new_population.append(SolutionGA(fitness=0, population=result['c2']))
        return new_population

    def __find_two_parents(self) -> dict:
        parent1 = self.__get_parent()
        parent2 = self.__get_parent()
        return {"p1": copy.deepcopy(parent1), "p2": copy.deepcopy(parent2)}

    def __get_parent(self) -> List[SolutionArea]:
        random_index = random.randint(0, len(self.parent_list) - 1)
        return copy.deepcopy(self.parent_list[random_index])

    def create_offspring(self, parent1: List[SolutionArea], parent2: List[SolutionArea]) -> dict:
        random.shuffle(parent1)
        random.shuffle(parent2)
        if len(parent1) > len(parent2):
            # return dynamic_application_of_operators(shortest=parent2, longest=parent1)
            return uniform_crossover(shortest=parent2, longest=parent1)
        else:
            # return dynamic_application_of_operators(shortest=parent1, longest=parent2)
            return uniform_crossover(shortest=parent1, longest=parent2)
