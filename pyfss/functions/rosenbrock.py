from functions.function import Function


class Rosenbrock(Function):
    def __init__(self):
        self.lower_limit = -5
        self.upper_limit = 10
        self.type = 'minimization'

    def fitness(self, position):
        fitness_result = 0

        for i in range(0, len(position) - 1):
            fitness_result += 100 * ((position[i + 1] - (position[i] ** 2)) ** 2) + ((1 - position[i]) ** 2)

        return fitness_result

    def compare_fitness(self, fitness_1, fitness_2):
        return fitness_1 < fitness_2
