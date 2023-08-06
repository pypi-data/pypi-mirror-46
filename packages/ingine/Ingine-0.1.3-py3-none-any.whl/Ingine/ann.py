import numpy

import os

from keras.models import Sequential
from keras.layers import Dense
from keras import utils
from keras import models
import hashlib
import uuid

os.environ['KERAS_BACKEND'] = 'theano'


def hash_data(data):
    """
    Функция хеширования данных. Пригодится для хеширования входных данных для
    последующего сравнения.
    :param data:
    :return: hash
    """
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + data.encode()).hexdigest()


def get_categorizer(input_data: numpy.ndarray,
                    result_data: numpy.ndarray,
                    num_cat: int,
                    train_amount: float = 0.8,
                    model: models = Sequential(),
                    layers: list = None,
                    loss: str = "categorical_crossentropy",
                    optimizer: str = "SGD",
                    metrics: str = "accuracy",
                    batch_size: int = None,
                    epochs: int = 1) -> type(lambda a: a):
    """
    Возвращает по полученным параметрам функцию-классификатор
    :param input_data: numpy.ndarray
        Список с входными данными. Каждый элемент списка также может быть списком.
    :param result_data: numpy.ndarray
        Список с ожидаемыми данными. Каждый элемент списка также может быть списком.
    :param num_cat: int
        Количество ожидаемых категорий.
    :param train_amount: float, optional
        Размер обучающей выборки в диапазоне от 0 до 1. По умолчанию 0.8 (80%)
    :param model: keras.models, optional
        Модель из keras.models. По умолчанию Sequential (последовательная)
    :param layers: list, optional
        Список слоев в соответствующем порядке. Слои в списке должны соответствовать
        одному из типов слоёв в keras. По умолчанию используются два полносвязных слоя,
        один из которых по размеру равен количеству свойств объекта, а второй -
        количеству категорий.
    :param loss: string, optional
        Функция ошибки. Должна соответствовать одному из названий функций
        ошибки в keras. По умолчанию = "categorical_crossentrophy"
    :param optimizer: string, optional
        Функция оптимизации. Должна соответствовать одному из названий функций
        оптимизации в keras. По умолчанию = "SGD"
    :param metrics: string, optional
        Функция измерения точности. Должна соответствовать одному из названий метрик
        в keras. По умолчанию = "accuracy"
    :param batch_size: int, optional
        Размер пакета обрабатываемых за один раз обучающих примеров.
        По умолчанию составляет 0.5% от обучающей выборки. Если размер меньше 200,
        он автоматически становится равным 200.
    :param epochs: int, optional
        Количество эпох (циклов обучения на всех элементах выборки). По умолчанию = 1.
    :return: Функция-классификатор. Рекомендуется применять к ней декораторы.
    """
    # Получение отпечатка параметров. Служит для того, чтобы не обучать уже обученную модель.
    params = [a[1] for a in locals().items() if a[0] not in ('fingerprint', 'model')]
    fingerprint = hashlib.md5(str(params).encode()).hexdigest()

    # Попытка загрузить данные о сети, если она уже компилировалась на данном устройстве
    try:
        # Загружаем данные об архитектуре сети
        with open('presaved/%s.json' % fingerprint, "r") as json:
            model = json.read()
        # Создаем модель
        model = models.model_from_json(model)
        # Загружаем сохраненные веса в модель
        model.load_weights('presaved/%s.h5' % fingerprint)
        print("Данные о данной конфигурации сети обнаружены и загружены")
        return lambda a: model.predict(a)
    except FileNotFoundError:
        print("Данные о данной конфигурации сети НЕ обнаружены. Обучение.")

    # Получение размеров пакета и выборок
    idl = len(input_data)
    input_data_test = input_data[int(idl * train_amount):]
    input_data_train = input_data[:int(idl * train_amount)]
    features_num = len(input_data_train[0])
    batch_size = batch_size if batch_size else idl * 0.005
    batch_size = int(batch_size) if batch_size > 200 else 200

    rdl = len(result_data)
    result_data_test = result_data[int(rdl * train_amount):]
    result_data_train = result_data[:int(rdl * train_amount)]
    result_data_test = utils.to_categorical(result_data_test, num_cat)
    result_data_train = utils.to_categorical(result_data_train, num_cat)

    # Инициализация слоёв
    if layers:
        for layer in layers:
            model.add(layer)
    else:
        model.add(Dense(features_num, input_dim = features_num, activation = 'relu', kernel_initializer = "normal"))
        model.add(Dense(num_cat, input_dim = num_cat, activation = "softmax", kernel_initializer = "normal"))

    # Компиляция модели
    model.compile(loss = loss, optimizer = optimizer, metrics = [metrics])
    model.fit(input_data_train, result_data_train, batch_size = batch_size, epochs = epochs)

    # Вывод метрик
    scores = model.evaluate(input_data_test, result_data_test, verbose = 1)
    print(scores)

    # сохранение модели
    try:
        os.mkdir('presaved')
    except FileExistsError:
        pass
    with open('presaved/%s.json' % fingerprint, 'w') as f:
        f.write(model.to_json())
    model.save_weights('presaved/%s.h5' % fingerprint)

    return lambda a: model.predict(a)


def get_regression(input_data: numpy.ndarray,
                   result_data: numpy.ndarray,
                   train_amount: float = 0.8,
                   model: models = Sequential(),
                   layers: list = None,
                   loss: str = "mse",
                   optimizer: str = "adam",
                   metrics: str = "mse",
                   batch_size: int = None,
                   epochs: int = 1) -> type(lambda a: a):
    """
    Возвращает по полученным параметрам функцию-классификатор
    :param input_data: numpy.ndarray
        Список с входными данными. Каждый элемент списка также может быть списком.
    :param result_data: numpy.ndarray
        Список с ожидаемыми данными. Каждый элемент списка также может быть списком.
    :param train_amount: float, optional
        Размер обучающей выборки в диапазоне от 0 до 1. По умолчанию 0.8 (80%)
    :param model: keras.models, optional
        Модель из keras.models. По умолчанию Sequential (последовательная)
    :param layers: list, optional
        Список слоев в соответствующем порядке. Слои в списке должны соответствовать
        одному из типов слоёв в keras. По умолчанию используются два полносвязных слоя,
        один из которых по размеру равен количеству свойств объекта, а второй -
        выходному значению.
    :param loss: string, optional
        Функция ошибки. Должна соответствовать одному из названий функций
        ошибки в keras. По умолчанию = "mse" - среднеквадратичная
    :param optimizer: string, optional
        Функция оптимизации. Должна соответствовать одному из названий функций
        оптимизации в keras. По умолчанию = "adam"
    :param metrics: string, optional
        Функция измерения точности. Должна соответствовать одному из названий метрик
        в keras. По умолчанию = "mse" - среднеквадратичная
    :param batch_size: int, optional
        Размер пакета обрабатываемых за один раз обучающих примеров.
        По умолчанию составляет 0.5% от обучающей выборки. Если размер меньше 200,
        он автоматически становится равным 200.
    :param epochs: int, optional
        Количество эпох (циклов обучения на всех элементах выборки). По умолчанию = 1.
    :return: Функция-классификатор. Рекомендуется применять к ней декораторы.
    """
    # Получение отпечатка параметров. Служит для того, чтобы не обучать уже обученную модель.
    params = [a[1] for a in locals().items() if a[0] not in ('fingerprint', 'model')]
    fingerprint = hashlib.md5(str(params).encode()).hexdigest()

    # Попытка загрузить данные о сети, если она уже компилировалась на данном устройстве
    try:
        # Загружаем данные об архитектуре сети
        with open('presaved/%s.json' % fingerprint, "r") as json:
            model = json.read()
        # Создаем модель
        model = models.model_from_json(model)
        # Загружаем сохраненные веса в модель
        model.load_weights('presaved/%s.h5' % fingerprint)
        print("Данные о данной конфигурации сети обнаружены и загружены")
        return lambda a: model.predict(a)
    except FileNotFoundError:
        print("Данные о данной конфигурации сети НЕ обнаружены. Обучение.")

    # Получение размеров пакета и выборок
    idl = len(input_data)
    input_data_test = input_data[int(idl * train_amount):]
    input_data_train = input_data[:int(idl * train_amount)]
    features_num = len(input_data_train[0])
    batch_size = batch_size if batch_size else idl * 0.005
    batch_size = int(batch_size) if batch_size > 200 else 200

    rdl = len(result_data)
    result_data_test = result_data[int(rdl * train_amount):]
    result_data_train = result_data[:int(rdl * train_amount)]

    # Инициализация слоёв
    if layers:
        for layer in layers:
            model.add(layer)
    else:
        model.add(Dense((features_num - 1) ** 2, input_dim = features_num, activation = 'relu',
                        kernel_initializer = "normal"))
        model.add(Dense(1))

    # Компиляция модели
    model.compile(loss = loss, optimizer = optimizer, metrics = [metrics])
    model.fit(input_data_train, result_data_train, batch_size = batch_size, epochs = epochs)

    # Вывод метрик
    scores = model.evaluate(input_data_test, result_data_test, verbose = 1)
    print(scores)

    # сохранение модели
    try:
        os.mkdir('presaved')
    except FileExistsError:
        pass
    with open('presaved/%s.json' % fingerprint, 'w') as f:
        f.write(model.to_json())
    model.save_weights('presaved/%s.h5' % fingerprint)

    return lambda a: model.predict(a)


def get_customnn(input_data: numpy.ndarray,
                 result_data: numpy.ndarray,
                 layers: list,
                 train_amount: float = 0.8,
                 model: models = Sequential(),
                 loss: str = "mae",
                 optimizer: str = "SGD",
                 metrics: str = "mse",
                 batch_size: int = None,
                 epochs: int = 1) -> type(lambda a: a):
    """
    Возвращает по полученным параметрам функцию нейронной сети с пользовательскими слоями.
    :param input_data: numpy.ndarray
        Список с входными данными. Каждый элемент списка также может быть списком.
    :param result_data: numpy.ndarray
        Список с ожидаемыми данными. Каждый элемент списка также может быть списком.
    :param layers: list
        Список слоев в соответствующем порядке. Слои в списке должны соответствовать
        одному из типов слоёв в keras.
    :param train_amount: float, optional
        Размер обучающей выборки в диапазоне от 0 до 1. По умолчанию 0.8 (80%)
    :param model: keras.models, optional
        Модель из keras.models. По умолчанию Sequential (последовательная)
    :param loss: string, optional
        Функция ошибки. Должна соответствовать одному из названий функций
        ошибки в keras. По умолчанию = "mae"
    :param optimizer: string, optional
        Функция оптимизации. Должна соответствовать одному из названий функций
        оптимизации в keras. По умолчанию = "SGD"
    :param metrics: string, optional
        Функция измерения точности. Должна соответствовать одному из названий метрик
        в keras. По умолчанию = "mse"
    :param batch_size: int, optional
        Размер пакета обрабатываемых за один раз обучающих примеров.
        По умолчанию составляет 0.5% от обучающей выборки. Если размер меньше 200,
        он автоматически становится равным 200.
    :param epochs: int, optional
        Количество эпох (циклов обучения на всех элементах выборки). По умолчанию = 1.
    :return: Функция-классификатор. Рекомендуется применять к ней декораторы.
    """
    # Получение отпечатка параметров. Служит для того, чтобы не обучать уже обученную модель.
    params = [a[1] for a in locals().items() if a[0] not in ('fingerprint', 'model')]
    print(params)
    fingerprint = hashlib.md5(str(params).encode()).hexdigest()

    # Попытка загрузить данные о сети, если она уже компилировалась на данном устройстве
    try:
        # Загружаем данные об архитектуре сети
        with open('presaved/%s.json' % fingerprint, "r") as json:
            model = json.read()
        # Создаем модель
        model = models.model_from_json(model)
        # Загружаем сохраненные веса в модель
        model.load_weights('presaved/%s.h5' % fingerprint)
        print("Данные о данной конфигурации сети обнаружены и загружены")
        return lambda a: model.predict(a)
    except FileNotFoundError:
        print("Данные о данной конфигурации сети НЕ обнаружены. Обучение.")

    # Получение размеров пакета и выборок
    idl = len(input_data)
    input_data_test = input_data[int(idl * train_amount):]
    input_data_train = input_data[:int(idl * train_amount)]
    features_num = len(input_data_train[0])
    batch_size = batch_size if batch_size else idl * 0.005
    batch_size = int(batch_size) if batch_size > 200 else 200

    rdl = len(result_data)
    result_data_test = result_data[int(rdl * train_amount):]
    result_data_train = result_data[:int(rdl * train_amount)]

    for layer in layers:
        model.add(layer)

    # Компиляция модели
    model.compile(loss = loss, optimizer = optimizer, metrics = [metrics])
    model.fit(input_data_train, result_data_train, batch_size = batch_size, epochs = epochs)

    # Вывод метрик
    scores = model.evaluate(input_data_test, result_data_test, verbose = 1)
    print(scores)

    # сохранение модели
    try:
        os.mkdir('presaved')
    except FileExistsError:
        pass
    with open('presaved/%s.json' % fingerprint, 'w') as f:
        f.write(model.to_json())
    model.save_weights('presaved/%s.h5' % fingerprint)

    return lambda a: model.predict(a)
