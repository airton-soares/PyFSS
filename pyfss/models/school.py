from models.fish import Fish


class School:
    def __init__(self, size, dimension, lower_limit, upper_limit, max_num_iterations):
        self.fishes = [Fish(dimension, lower_limit, upper_limit, max_num_iterations) for _ in range(size)]
        self.__update_weight()

    def __update_weight(self):
        self.total_weight = sum([fish.weight for fish in self.fishes])
