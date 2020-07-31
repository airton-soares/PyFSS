import random


def search(function, school, init_ind_step, final_ind_step, init_vol_step, final_vol_step, max_num_iterations):
    best_fitness = None
    step_ind = init_ind_step
    step_vol = init_vol_step
    school_weight = sum(list(map(lambda curr_fish: curr_fish.weight, school.fishes)))
    iteration = 0

    while iteration < max_num_iterations:
        iteration += 1
        max_fitness_variation = 0
        fitness_variation_sum = 0

        for fish in school.fishes:
            __move_fish_ind(fish, step_ind, function)

            if max_fitness_variation < fish.fitness_variation:
                max_fitness_variation = fish.fitness_variation

            fitness_variation_sum += fish.fitness_variation

        for fish in school.fishes:
            __feed_fish(fish, max_fitness_variation, max_num_iterations)

            if fitness_variation_sum != 0:
                __move_fish_inst(fish, fitness_variation_sum, function.lower_limit, function.upper_limit)

        new_school_weight = sum(list(map(lambda curr_fish: curr_fish.weight, school.fishes)))
        barycenter = __calculate_barycenter(school, new_school_weight)

        for fish in school.fishes:
            __move_fish_vol(fish, barycenter, step_vol, function.lower_limit, function.upper_limit, new_school_weight > school_weight)

        school_weight = new_school_weight
        curr_best_fitness = __best_fitness(school, function)

        if best_fitness is None or function.compare_fitness(curr_best_fitness, best_fitness):
            best_fitness = curr_best_fitness

        step_ind -= (init_ind_step - final_ind_step) / max_num_iterations
        step_vol -= (init_vol_step - final_vol_step) / max_num_iterations

    return best_fitness


def __move_fish_ind(fish, step_ind, function):
    new_position = []

    for coord in fish.position:
        new_coord = coord + random.uniform(-1, 1) * step_ind

        if new_coord < function.lower_limit:
            new_position.append(function.lower_limit)
        elif new_coord > function.upper_limit:
            new_position.append(function.upper_limit)
        else:
            new_position.append(new_coord)

    fitness = function.fitness(fish.position)
    new_fitness = function.fitness(new_position)

    if new_fitness < fitness:
        last_position = fish.position.copy()
        fish.position = new_position
        fish.position_variation = [last_position_i - fish.position_i for last_position_i, fish.position_i in zip(last_position, fish.position)]

        if function.type == 'minimization':
            fish.fitness_variation = fitness - new_fitness
        else:
            fish.fitness_variation = new_fitness - fitness
    else:
        fish.position_variation = [0 for _ in range(len(fish.position))]
        fish.fitness_variation = 0


def __move_fish_inst(fish, fitness_variation_sum, lower_limit, upper_limit):
    inst_vector = [(coord * fish.fitness_variation) / fitness_variation_sum for coord in fish.position_variation]
    new_position = []

    for i in range(0, len(fish.position)):
        new_coord = fish.position[i] + inst_vector[i]

        if new_coord < lower_limit:
            new_position.append(lower_limit)
        elif new_coord > upper_limit:
            new_position.append(upper_limit)
        else:
            new_position.append(new_coord)

    fish.position = new_position


def __move_fish_vol(fish, barycenter, step_vol, lower_limit, upper_limit, weight_gain):
    new_position = []

    for i in range(0, len(fish.position)):
        if weight_gain:
            new_coord = fish.position[i] - (random.uniform(0, 1) * step_vol * (fish.position[i] - barycenter[i]))
        else:
            new_coord = fish.position[i] + (random.uniform(0, 1) * step_vol * (fish.position[i] - barycenter[i]))

        if new_coord < lower_limit:
            new_position.append(lower_limit)
        elif new_coord > upper_limit:
            new_position.append(upper_limit)
        else:
            new_position.append(new_coord)

    fish.position = new_position


def __feed_fish(fish, max_fitness_variation, max_num_iterations):
    new_weight = None

    if max_fitness_variation != 0:
        if max_fitness_variation < 0:
            if fish.fitness_variation < 0:
                fitness_variation = -2 * fish.fitness_variation
            else:
                fitness_variation = fish.fitness_variation

            new_weight = fish.weight + fitness_variation / max_fitness_variation
        else:
            new_weight = fish.weight + fish.fitness_variation / max_fitness_variation

    if new_weight is not None:
        if new_weight < 1:
            fish.weight = 1
        elif new_weight > max_num_iterations / 2:
            fish.weight = max_num_iterations / 2
        else:
            fish.weight = new_weight


def __calculate_barycenter(school, school_weight):
    weighted_positions = list(map(lambda fish: [coord * fish.weight for coord in fish.position], school.fishes))
    origin_position = [0 for _ in range(len(school.fishes[0].position))]
    return [coord / school_weight for coord in __lists_sum(origin_position, weighted_positions)]


def __best_fitness(school, function):
    best_fitness = None

    for fish in school.fishes:
        curr_fitness = function.fitness(fish.position)

        if best_fitness is None or function.compare_fitness(curr_fitness, best_fitness):
            best_fitness = curr_fitness

    return best_fitness


def __lists_sum(result, lists):
    if not lists:
        return result
    else:
        curr_list, *lists_tail = lists
        result = [result_i + curr_list_i for result_i, curr_list_i in zip(result, curr_list)]
        return __lists_sum(result, lists_tail)
