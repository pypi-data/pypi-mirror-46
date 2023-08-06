from pyeasyga.pyeasyga import GeneticAlgorithm


def get_optimizer(data: list,
                  fitness: type(lambda a: a),
                  population_size: int = 10,
                  generations: int = 100,
                  crossover_probability: float = 0.8,
                  mutation_probability: float = 0.05,
                  elitism: bool = True,
                  maximise_fitness: bool = True,
                  create_individual: type(lambda a: a) = None,
                  crossover: type(lambda a: a) = None,
                  mutate: type(lambda a: a) = None,
                  selection: type(lambda a: a) = None) -> type(lambda a: a):
    """
    :return: ga
        Возвращает объект ga. Методы искать в документации pyeasyga.
    :param data: anything
        Пример существа, генома. Может быть списков.
    :param fitness: function
        Функция приспособленности.
    :param population_size: int, optional
        Размер популяции. По умолчанию равен 10.
    :param generations: int, optional
        Количество поколений. По умолчанию равно 100.
    :param crossover_probability: float, optional
        Вероятность скрещивания. По умолчанию равна 0.8.
    :param mutation_probability: float, optional
        Вероятность мутации. По умолчанию равна 0.05.
    :param elitism: bool, optional
        Применение стратегии элитизма. По умолчанию True.
    :param maximise_fitness: bool, optional
        Ориентирование на увеличение или уменьшение значения фитнесс-функции.
        По умолчанию True.
    :param create_individual: function, optional
        Функция, позволяющая создать случайное существо из data.
        По умолчанию взята из пакета pyeasyga.
    :param crossover: function, optional
        Функция скрещивания.
        По умолчанию взята из пакета pyeasyga.
    :param mutate:
    function, optional
        Функция мутации.
        По умолчанию взята из пакета pyeasyga.
    :param selection: function, optional
        Функция селекции.
        По умолчанию взята из пакета pyeasyga (random selection).
    """

    ga = GeneticAlgorithm(data,
                          population_size = population_size,
                          generations = generations,
                          crossover_probability = crossover_probability,
                          mutation_probability = mutation_probability,
                          elitism = elitism,
                          maximise_fitness = maximise_fitness)
    ga.create_individual = create_individual if create_individual else ga.create_individual
    ga.crossover_function = crossover if crossover else ga.crossover_function
    ga.mutate_function = mutate if mutate else ga.mutate_function
    ga.selection_function = selection if selection else ga.selection_function
    ga.fitness_function = fitness
    ga.run()

    return ga.best_individual
