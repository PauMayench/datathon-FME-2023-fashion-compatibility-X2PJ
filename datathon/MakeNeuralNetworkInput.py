import cv2
import os
import numpy as np
import random


from classes import Product
from utils import obtenirDades, outfitImage, generateListRandomOutfits

#generates an image given a dictionary of products,  the id of the outfit that will be the name of the image, the folder "class" where you  want to store the image,
def generateAndSave(product_dict, outfitId, classId):
	finalImage = outfitImage(product_dict)
	finalImage = cv2.resize(finalImage,(int(finalImage.shape[1]/2), int(finalImage.shape[0]/2)))
	cv2.imwrite(os.path.join(os.getcwd(), "class"+str(classId), str(outfitId)+".jpg"), finalImage)



'''
This python code creates from the csv all the images of the outfits, and stores them on a directory called class1,
then it creates the same amount of outfits generated randomly with some restrictions, these outfits will be given 
to the model as "bad" outfits and are stored on class2
'''


dict_outfits, dict_prendas = obtenirDades() # we read the data form the csv

#if the folders dont exist we create them
if not os.path.exists("class1"):
        os.makedirs("class1")

if not os.path.exists("class2"):
        os.makedirs("class2")

#Generating "good" outfits
for outfit in dict_outfits.values():		#for each outfit we create an image so we can train the model
	prendas = outfit.products
	outfitId = outfit.cod_outfit
	generateAndSave(prendas, outfitId, 1)



#Generating "bad" outfits

list_prendas = list(dict_prendas.values())

list_dicts_products = generateListRandomOutfits(len(dict_outfits), list_prendas)


for i, product_dict in enumerate(list_dicts_products):
	generateAndSave(product_dict,i,2) #we save the outfit on class2