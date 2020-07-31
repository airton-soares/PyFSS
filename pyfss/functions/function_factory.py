from functions.function_type import FunctionType
from functions.rastrigin import Rastrigin
from functions.rosenbrock import Rosenbrock


def build_function(typ):
    if typ == FunctionType.ROSENBROCK.value:
        return Rosenbrock()
    elif typ == FunctionType.RASTRIGIN.value:
        return Rastrigin()
