from abc import ABC, abstractmethod


class Function(ABC):
    @abstractmethod
    def fitness(self, position):
        pass

    @abstractmethod
    def compare_fitness(self, fitness_1, fitness_2):
        pass
