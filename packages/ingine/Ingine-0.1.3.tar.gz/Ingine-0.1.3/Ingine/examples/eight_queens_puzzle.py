import random
from pyeasyga import pyeasyga
from Ingine import ga

# setup seed data
data = [0, 1, 2, 3, 4, 5, 6, 7]

# initialise the GA
gaa = pyeasyga.GeneticAlgorithm(data,
                                population_size = 200,
                                generations = 100,
                                crossover_probability = 0.8,
                                mutation_probability = 0.2,
                                elitism = True,
                                maximise_fitness = False)


# define and set function to create a candidate solution representation
def create_individual(data):
    individual = data[:]
    random.shuffle(individual)
    return individual


def crossover(parent_1, parent_2):
    crossover_index = random.randrange(1, len(parent_1))
    child_1a = parent_1[:crossover_index]
    child_1b = [i for i in parent_2 if i not in child_1a]
    child_1 = child_1a + child_1b

    child_2a = parent_2[crossover_index:]
    child_2b = [i for i in parent_1 if i not in child_2a]
    child_2 = child_2a + child_2b

    return child_1, child_2


def mutate(individual):
    mutate_index1 = random.randrange(len(individual))
    mutate_index2 = random.randrange(len(individual))
    individual[mutate_index1], individual[mutate_index2] = individual[mutate_index2], individual[mutate_index1]


def selection(population):
    return random.choice(population)


def fitness(individual, data):
    collisions = 0
    for item in individual:
        item_index = individual.index(item)
        for elem in individual:
            elem_index = individual.index(elem)
            if item_index != elem_index:
                if item - (elem_index - item_index) == elem\
                        or (elem_index - item_index) + item == elem:
                    collisions += 1
    return collisions


def print_board(board_representation):
    def print_x_in_row(row_length, x_position):
        print('-' + ''.join(['----' for _ in range(row_length)]))
        print('|' + ''.join([' X |' if i == x_position else '   |' for i in range(row_length)])),

    def print_board_bottom(row_length):
        print('-' + ''.join(['----' for _ in range(row_length)]))

    num_of_rows = len(board_representation)
    row_length = num_of_rows  #rows == columns in a chessboard

    for row in range(num_of_rows):
        print_x_in_row(row_length, board_representation[row])

    print_board_bottom(row_length)
    print('\n')


optimizer = ga.get_optimizer(data,
                             population_size = 200,
                             generations = 100,
                             crossover_probability = 0.8,
                             mutation_probability = 0.2,
                             elitism = True,
                             maximise_fitness = False,
                             create_individual = create_individual,
                             crossover = crossover,
                             mutate = mutate,
                             fitness = fitness,
                             selection = selection)

res = optimizer()

# print the GA's best solution; a solution is valid only if there are no collisions
if res[0] == 0:
    print(res)
    print_board(res[1])
else:
    print(None)
