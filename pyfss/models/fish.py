import random


class Fish:
    def __init__(self, dimension, lower_limit, upper_limit, max_num_iterations):
        self.weight = max_num_iterations / 4
        self.position = [random.uniform(lower_limit, upper_limit) for _ in range(dimension)]
        self.position_variation = [0 for _ in range(dimension)]
        self.fitness_variation = 0.0
