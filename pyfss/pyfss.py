import os
import fss
import time
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from functions.function_factory import build_function
from functions.function_type import FunctionType
from models.school import School


def build_args_parser():
    usage = 'python pyfss.py -d <dimension>\n       ' \
            'run with --help for arguments descriptions'
    parser = ArgumentParser(description='A Python implementation of the Fish School Search algorithm', usage=usage)

    parser.add_argument('-s', '--school', dest='school_size', type=int, default=30,
                        help='Size of the school')
    parser.add_argument('--init_ind_step', dest='init_ind_step', type=float, default=0.1,
                        help='Initial individual step')
    parser.add_argument('--final_ind_step', dest='final_ind_step', type=int, default=0.001,
                        help='Final individual step')
    parser.add_argument('--init_vol_step', dest='init_vol_step', type=float, default=0.1,
                        help='Initial volitional step')
    parser.add_argument('--final_vol_step', dest='final_vol_step', type=int, default=0.001,
                        help='Final volitional step')
    parser.add_argument('-i', '--iterations', dest='max_num_iterations', type=int, default=10000,
                        help='Maximum number of iterations in the search')
    parser.add_argument('-d', '--dimension', dest='dimension', type=int, default=30,
                        help='Dimension of the functions input')
    parser.add_argument('--simulations', dest='num_simulations', type=int, default=30,
                        help='Number of simulations to be done for the optimization')

    return parser


def main():
    args_parser = build_args_parser()
    args = args_parser.parse_args()
    results_dir_path = "results"

    if not os.path.exists(results_dir_path):
        os.makedirs(results_dir_path)

    for function_type in [f.value for f in FunctionType]:
        function = build_function(function_type)
        best_fitness_list = []

        for i in range(args.num_simulations):
            start_time = time.time()

            school = School(args.school_size, args.dimension, function.lower_limit, function.upper_limit,
                            args.max_num_iterations)
            best_fitness = fss.search(function, school, args.init_ind_step, args.final_ind_step, args.init_vol_step,
                                      args.final_vol_step, args.max_num_iterations)

            elapsed_time = time.time() - start_time

            print(function_type + ", simulação: " + str(i + 1) + ", fitness: " + str(round(best_fitness, 2)) + "(" +
                  str(round(elapsed_time, 2)) + " s)")

            best_fitness_list.append(best_fitness)

        plt.clf()
        plt.boxplot(best_fitness_list)
        plt.title(function_type)
        plt.savefig(os.path.join(results_dir_path, function_type + "_box_plot.png"), bbox_inches='tight')


if __name__ == '__main__':
    main()
