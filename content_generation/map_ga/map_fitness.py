import random

class MapFitness:

    def calculate_fitness_for_all(self, population_dict, surface_dict, blocks_dict):
        for population in population_dict:
            self.calculate_individual_fitness(population)

    def calculate_individual_fitness(self, dict_index):
        # population = dict_index['population']
        dict_index['fitness'] = self.calculate_fitness_from_population(dict_index['population'])

    def calculate_fitness_from_population(self, population):

        return random.randint(1, 10000)
