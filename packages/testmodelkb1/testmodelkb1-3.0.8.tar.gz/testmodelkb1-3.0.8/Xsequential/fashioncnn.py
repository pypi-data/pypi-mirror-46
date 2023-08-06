# -*- coding: utf-8 -*-
"""
Test for Keras Image classification
"""
# TensorFlow and keras
import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.utils import plot_model
from keras.models import load_model
import Xsequential


# Helper libraries
#import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# import Fashion MINST from keras
fashion_mnist = keras.datasets.fashion_mnist

# divide datasets into train and evaluation

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# scale the images
train_images = train_images / 255.0
test_images = test_images / 255.0



# build the model
def createmodel():

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model

model = createmodel()
model.compile(optimizer='sgd',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


model.start_experiment("owner", "FashionMnist", "dataset_link", "sclink")
history = model.xfit(train_images, train_labels, epochs=2, batch_size=32)

model.save('fashioncnn.h5')