import os
import numpy

from keras.datasets import boston_housing
from keras import utils
from Ingine import ann

os.environ['KERAS_BACKEND'] = 'theano'

# Загружаем данные
(x_train, y_train), (x_test, y_test) = boston_housing.load_data()

# Среднее значение
mean = x_train.mean(axis=0)
# Стандартное отклонение
std = x_train.std(axis=0)
x_train -= mean
x_train /= std
x_test -= mean
x_test /= std

regression = ann.get_regression(x_train, y_train, epochs = 101, loss = 'mse')

print(regression(x_test[50].reshape(1, 13))[0], y_test[50])