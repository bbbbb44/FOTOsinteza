# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from pathlib import Path
import os
import glob
import cv2
from PIL import Image

def napolniTrainingInTestingImages(potDoDatabasea,imenaRastlin, imgWidth, imgHeight):


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
    imgWidth = 400
    imgHeight = 400
    potDoDatabasea="/home/besko/Šola/asd/FOTOsinteza-main/SUDO_MEME_CRAWLER/Dataset"
    imenaRastlin=["Daylilies", "Iris"]
    training_images, validation_images = napolniTrainingInTestingImages(potDoDatabasea,imenaRastlin,imgWidth, imgHeight)


    model = models.Sequential()
    model.add(layers.experimental.preprocessing.Rescaling(1./255))
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3))) # Input layer, slike so zaenkrat 32x32
    model.add(layers.MaxPooling2D((2, 2))) # Maxpooling layer ki poenostavi rezultate activation layerja
    model.add(layers.Conv2D(64, (3, 3), activation='relu')) # Activation relu layer
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten()) # Iz matrike naredimo enodimenzijonalen array
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10,activation='softmax')) # Output layer, softmax normalizira rezultate med 0-1

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy']) # Compilamo model, gledamo natančnost
    model.fit(training_images, epochs=30, validation_data=validation_images) # Poženemo model, epochs je št. ponovitev


    # loss, accuracy = model.evaluate(testing_images, testing_labels)
    # print("Loss: ")
    # print(loss)
    # print("Accuracy: ")
    # print(accuracy)

    model.save('image_classifier.model')
