# This Python file uses the following encoding: utf-8
import sys
import time
import base64
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from tensorflow.keras import datasets, layers, models
import pymongo
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

def resetAllFkPlants(mycol):
        myquery = {}
        newvalues = { "$set": { "fk_plant": "-1" } }
        print("RESET ALL FK_PLANTS")
        x = mycol.update_many(myquery, newvalues)
		
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
    mydb = myclient["projekt"]
    mycol = mydb["images"]

    # resetAllFkPlants(mycol)
    # SAMO ĆE ŽELIŠ RESET-AT VSE INDEXE

    lokacijaSlik = "/projekt/app/public/"
    while(1):
        time.sleep(1) # sleepam za 1 sekundo
        myquery1 = {"fk_plant": "-1"}
        myquery2 = {"metaPodatki": "1"}
        myquery3 = {"uploaded": "0"}
        mydoc1 = mycol.find(myquery1)
        mydoc2 = mycol.find(myquery2)
        mydoc3 = mycol.find(myquery3)
        for var in mydoc1: # RAZPOZAVANJE RASTLIN
            print(var['_id'])
            try:            
                myquery = { "_id": var['_id'] } # Query za update_one
                imageString = lokacijaSlik + var['path']
                image = cv2.imread(imageString, 1) # Preberem sliko
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Model je natreniran na RGB slikah
                image = cv2.resize(image, (imgHeight, imgWidth)) # Resizam sliko za prepoznavo.
                prediction = model.predict(np.array([image])) # predictam
                index = np.argmax(prediction) # Najdem index maximalno aktiviranega softmaxa
                newvalues = { "$set": { "fk_plant": str(index.item()) } }
                mycol.update_one(myquery, newvalues) # Updateam image z prepoznanim fk_plants
            except Exception as e:
                print("Exception ", e)


        for var in mydoc2: # GEO LOKACIJA
            print(var['_id'])
            myquery = { "_id": var['_id'] } # Query za update_one
            imageString = lokacijaSlik + var['path']
            try:
                img = Image.open(imageString)
                exif = img._getexif()
                geoTags = {}
                for (id, tag) in TAGS.items():
                    if tag == 'GPSInfo':
                        for (key, val) in GPSTAGS.items():
                            if key in exif[id]:
                                geoTags[val] = exif[id][key]
                latitude = (geoTags['GPSLatitude'])[0] + ((geoTags['GPSLatitude'])[1] / 60.0) + ((geoTags['GPSLatitude'])[2] / 3600.0)
                longitude = (geoTags['GPSLongitude'])[0] + ((geoTags['GPSLongitude'])[1] / 60.0) + ((geoTags['GPSLongitude'])[2] / 3600.0)
                if geoTags['GPSLatitudeRef'] == 'S':
                    latitude = -latitude
                if geoTags['GPSLongitudeRef'] == 'W':
                    longitude = - longitude
                newvalues = { "$set": { "metaPodatki": "0", "lat": longitude,"lon": latitude}  }
                print(latitude)
            except Exception as e:
                print("exception: ", e)
                newvalues = { "$set": { "metaPodatki": "-1" } }
            mycol.update_one(myquery, newvalues) # update

        for var in mydoc3: # UPLOADANJE
            myquery = { "_id": var['_id'] } # Query za update_one
            id = var['_id']
            print(id)
            data =(var['path'])
            imgdata = base64.b64decode(data)
            newPath = 'images/' + str(id) + 'u'
            pathDoSlike = '/projekt/app/public/images/' + str(id) + 'u'
            with open(pathDoSlike, 'wb') as f:
                f.write(imgdata) 
            newvalues = { "$set": { "uploaded": "1", "path": newPath} }
            mycol.update_one(myquery, newvalues) # update
