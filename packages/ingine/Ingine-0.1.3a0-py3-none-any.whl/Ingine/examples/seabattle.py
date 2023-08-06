import numpy

import os

os.environ['KERAS_BACKEND'] = 'theano'

from keras.layers import Dense
import csv

from Ingine import ann

# Устанавливаем seed для повторяемости результатов
numpy.random.seed(151681)


def load_data():
    """
    Функция получения данных из data.py
    :return: list(2) of lists(2)
    """
    input_data = []
    output_data = []

    from data import data

    data = [_.split(';') for _ in data.split('\n')]

    for row in data:
        in_data = row[0]
        out_data = row[1]
        in_data = in_data.replace('X', '1')
        in_data = in_data.replace('+', '1')
        in_data = in_data.replace('_', '0')
        in_data = in_data.replace('-', '0')

        out_data = out_data.replace('X', '0')
        out_data = out_data.replace('+', '0')
        out_data = out_data.replace('O', '1')
        out_data = out_data.replace('_', '0')
        out_data = out_data.replace('-', '0')

        in_data = list(map(lambda a: int(a), in_data))
        out_data = list(map(lambda a: int(a), out_data))

        input_data.append(in_data)
        output_data.append(out_data)

    input_data = numpy.asarray(input_data)
    output_data = numpy.asarray(output_data)

    input_data_test = input_data[8000:]
    input_data = input_data[:8000]

    output_data_test = output_data[8000:]
    output_data = output_data[:8000]

    return (input_data, output_data), (input_data_test, output_data_test)


# Загружаем данные
(X_train, Y_train), (X_test, Y_test) = load_data()

# Определеяем слои
layers = [Dense(100, input_dim = 100, activation = "softsign", kernel_initializer = "normal"),
          Dense(20, activation = "softsign", kernel_initializer = "normal"),
          Dense(10, activation = "softsign", kernel_initializer = "normal"),
          Dense(100, activation = "softsign", kernel_initializer = "normal")]

# Получение модели с
customnn = ann.get_customnn(X_train, Y_train, layers = layers, epochs = 5)

res = customnn(X_test)

xt = numpy.asarray([255 if a == 1 else a for a in X_test[15]]).reshape(10, 10)
yt = numpy.asarray([255 if a == 1 else a for a in Y_test[15]]).reshape(10, 10)
rt = numpy.asarray([int(-numpy.sign(a)) * 255 for a in res[15]]).reshape(10, 10)

from PIL import Image, ImageDraw

image = Image.new("L", (500, 500), (255,))
draw = ImageDraw.Draw(image)
for i in range(10):  # For every pixel:
    for j in range(10):
        draw.rectangle((i * 50, j * 50, (i + 1) * 50, (j + 1) * 50), fill = (xt[i][j],))

image.save("images/xt.png", "PNG")

image = Image.new("L", (500, 500), (255,))
draw = ImageDraw.Draw(image)
for i in range(10):  # For every pixel:
    for j in range(10):
        draw.rectangle((i * 50, j * 50, (i + 1) * 50, (j + 1) * 50), fill = (yt[i][j],))

image.save("images/yt.png", "PNG")

image = Image.new("L", (500, 500), (255,))
draw = ImageDraw.Draw(image)
for i in range(10):  # For every pixel:
    for j in range(10):
        draw.rectangle((i * 50, j * 50, (i + 1) * 50, (j + 1) * 50), fill = (rt[i][j],))

image.save("images/rt.png", "PNG")
