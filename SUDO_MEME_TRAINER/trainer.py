# This Python file uses the following encoding: utf-8
import sys
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from pathlib import Path
import os
import glob
import cv2
from PIL import Image

def napolniTrainingInTestingImages(potDoDatabasea, imgWidth, imgHeight):
    # Narejeno s pomočjo https://www.tensorflow.org/tutorials/load_data/images
    # Napolnim model iz podanega direktorija, 20% gre za validation, 80% za training, slike so rgb, label-i so int, seed potrebujem za split med validation in trainingom
    training_images = tf.keras.preprocessing.image_dataset_from_directory(
        potDoDatabasea, labels='inferred', label_mode='int',
        class_names=None, color_mode='rgb', batch_size=32, image_size=(imgHeight,imgWidth),
        shuffle=True, seed=4444, validation_split=0.2, subset="training",
        interpolation='bilinear', follow_links=False
    )
    validation_images = tf.keras.preprocessing.image_dataset_from_directory(
        potDoDatabasea, labels='inferred', label_mode='int',
        class_names=None, color_mode='rgb', batch_size=32, image_size=(imgHeight,imgWidth),
        shuffle=True, seed=4444, validation_split=0.2, subset="validation",
        interpolation='bilinear', follow_links=False
    )

    return training_images, validation_images
if __name__ == "__main__":
    imgWidth = 400 # width slike pri učenju modela
    imgHeight = 400 # height slike pri učenju modela
    potDoDatabasea="/python/TRAINER/DATASET" # pot do dataseta ki ga želimo uporabit.
    # Dataset ima strukturo -DATASET
    #                           -CLASS1
    #                               -image in class1
    #                               -image in class1
    #                           -CLASS2
    #                               -image in class2
    #                               -image in class2

    training_images, validation_images = napolniTrainingInTestingImages(potDoDatabasea,imgWidth, imgHeight)
    num_classes = len(training_images.class_names) # število classov
    # Narejeno s pomočjo https://www.tensorflow.org/tutorials/load_data/images ter https://www.youtube.com/watch?v=t0EzVCvQjGE
    model = models.Sequential()
    model.add(layers.experimental.preprocessing.Rescaling(1./255)) # rescaleam slik
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(imgHeight, imgWidth, 3))) # Input layer, input shape je slika heightxwidth ter 3 channels(barve)
    model.add(layers.MaxPooling2D((2, 2))) # Maxpooling layer ki poenostavi rezultate activation layerja
    model.add(layers.Conv2D(64, (3, 3), activation='relu')) # Activation relu layer
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten()) # Iz matrike naredimo enodimenzionalen array
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(num_classes,activation='softmax')) # Output layer, softmax normalizira rezultate med 0-1

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy']) # Compilamo model, gledamo natančnost
    model.fit(training_images, epochs=10, validation_data=validation_images) # Poženemo model, epochs je št. ponovitev

    loss, accuracy = model.evaluate(validation_images) # ocenim loss ter accuracy modela.
    print("Loss: ")
    print(loss)
    print("Accuracy: ")
    print(accuracy)
    classes = training_images.class_names
    for j in range(0, len(classes)):
        print(j, "-", classes[j])
    model.save('image_classifier.model')
