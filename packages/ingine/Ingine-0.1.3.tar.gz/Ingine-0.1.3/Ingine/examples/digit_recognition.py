import os
import numpy

from keras.datasets import mnist
from keras import utils
from Ingine import ann

os.environ['KERAS_BACKEND'] = 'theano'

# Загружаем данные
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Преобразование размерности изображений
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
# Нормализация данных
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

# Преобразуем метки в категории
Y_train = utils.to_categorical(y_train, 10)
Y_test = utils.to_categorical(y_test, 10)

categorizer = ann.get_categorizer(X_train, y_train, 10, epochs = 2)

print(categorizer(X_test[0].reshape(1, 784)))