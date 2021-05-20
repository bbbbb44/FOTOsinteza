# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models

if __name__ == "__main__":

    (training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data() # Zaenkrat še dataset iz cifar10 libraryja
    training_images = training_images / 255 # Normaliziram slike
    testing_images = testing_images / 255


    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3))) # Input layer, slike so zaenkrat 32x32
    model.add(layers.MaxPooling2D((2, 2))) # Maxpooling layer ki poenostavi rezultate activation layerja
    model.add(layers.Conv2D(64, (3, 3), activation='relu')) # Activation relu layer
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten()) # Iz matrike naredimo enodimenzijonalen array
    model.add(layers.Dense(64, activation='relu')) #
    model.add(layers.Dense(10,activation='softmax')) # Output layer, softmax normalizira rezultate med 0-1

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy']) # Compilamo model, gledamo natančnost
    model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels)) # Poženemo model, epochs je št. ponovitev


    loss, accuracy = model.evaluate(testing_images, testing_labels)
    print("Loss: ")
    print(loss)
    print("Accuracy: ")
    print(accuracy)

    model.save('image_classifier.model')
