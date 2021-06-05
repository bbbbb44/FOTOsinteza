# This Python file uses the following encoding: utf-8
import sys
import time
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models
import pymongo

if __name__ == "__main__":
    imgWidth = 400 # width slike
    modelName = "image_classifier.model"
    imgHeight = 400 # height slike
    model = models.load_model(modelName)

    # TO JE ZA TESTIRANJE
    # class_names = ['Dalhias', 'Daylilies', 'Iris', 'Roses', 'Salvias', 'Sempervivum']
    # print(sys.argv[1])
    # image = cv2.imread(sys.argv[1], 1)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Model je natreniran na RGB slikah

    # Prikaz slike
    # cv2.imshow('slika', image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # prediction = model.predict(np.array([image]))
    # index = np.argmax(prediction) # Najdem index maximalno aktiviranega softmaxa
    # print(class_names[index])


    myclient = pymongo.MongoClient("mongodb://localhost:27017")
    while(1):
        time.sleep(1) # sleepam za 1 sekundo
        mydb = myclient["projekt"]
        mycol = mydb["images"]
        myquery = {"fk_plant": "-1"}
        mydoc = mycol.find(myquery)
        for var in mydoc:
            print(var['_id'])
            myquery = { "_id": var['_id'] } # Query za update_one
            imageString = "/projekt/app/public/" + var['path']
            image = cv2.imread(imageString, 1) # Preberem sliko
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Model je natreniran na RGB slikah
            image = cv2.resize(image, (imgHeight, imgWidth)) # Resizam sliko za prepoznavo.
            prediction = model.predict(np.array([image])) # predictam
            index = np.argmax(prediction) # Najdem index maximalno aktiviranega softmaxa
            newvalues = { "$set": { "fk_plant": str(index.item()) } }
            mycol.update_one(myquery, newvalues) # Updateam image z prepoznanim fk_plants


