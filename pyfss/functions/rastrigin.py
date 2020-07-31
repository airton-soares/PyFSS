from functions.function import Function

import math


class Rastrigin(Function):
    def __init__(self):
        self.lower_limit = -5.12
        self.upper_limit = 5.12
        self.type = 'minimization'

    def fitness(self, position):
        dimension = len(position)
        return (10 * dimension) + sum([(coord ** 2) - 10 * math.cos(2 * math.pi * coord) for coord in position])

    def compare_fitness(self, fitness_1, fitness_2):
        return fitness_1 < fitness_2
