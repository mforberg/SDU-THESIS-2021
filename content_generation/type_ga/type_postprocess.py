from shared_variables import *


def run_postprocess(solution: SolutionGA, surface_dict: dict):
    for area in solution.population:
        check_for_digestible_areas(surface_dict=surface_dict, area=area, solution=solution)

def check_for_digestible_areas(solution: SolutionGA, area: SolutionArea, surface_dict: dict):
    pass
