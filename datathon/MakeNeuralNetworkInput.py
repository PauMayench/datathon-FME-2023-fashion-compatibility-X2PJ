import cv2
import os
import numpy as np
import random

from classes import Product
from utils import obtenirDades, outfitImage

#generates an image given a dictionary of products,  the id of the outfit that will be the name of the image, the folder "class" where you  want to store the image,
def generateAndSave(dict_prendas, outfitId, classId):
	finalImage = outfitImage(dict_prendas)
	finalImage = cv2.resize(finalImage,(int(finalImage.shape[1]/2), int(finalImage.shape[0]/2)))
	cv2.imwrite(os.path.join(os.getcwd(), "class"+str(classId), str(outfitId)+".jpg"), finalImage)

#filters a product list on diferent classified lists by category
def productFilter(product_list):
	top = []
	bottom = []
	dresses = []
	others = []
	for product in product_list:
		if product.des_product_category == "Tops":
			top.append(product)
		elif product.des_product_category == "Bottoms":
			bottom.append(product)
		elif product.des_product_category == "Dresses, jumpsuits and Complete set":
			bottom.append(product)
		else:
			others.append(product)

		
	return top, bottom, dresses, others

'''
This python code creates from the csv all the images of the outfits, and stores them on a directory called class1,
then it creates the same amount of outfits generated randomly with some restrictions, these outfits will be given 
to the model as "bad" outfits and are stored on class2
'''


dict_otufits, dict_prendas = obtenirDades() # we read the data form the csv

#if the folders dont exist we create them
if not os.path.exists("class1"):
        os.makedirs("class1")

if not os.path.exists("class2"):
        os.makedirs("class2")

#Generating "good" outfits
for outfit in dict_otufits.values():		#for each outfit we create an image so we can train the model
	prendas = outfit.prendas
	outfitId = outfit.cod_outfit
	generateAndSave(prendas, outfitId, 1)



#Generating "bad" outfits

list_prendas = list(dict_prendas.values())
top, bottom, dresses, others = productFilter(list_prendas)


for i in range(len(dict_otufits)): #we make as many outfits as the original csv
	dist_prendes_outfit_random = {}

	rand_num = random.randint(2, 10)

	if rand_num > 8 or rand_num == 2:	# this reduces the chances of creating outfits with extreme number of products
		rand_num = random.randint(2, 10)

	if rand_num <= 5 and random.randint(1, 4) != 1: # if the number of products is small, most frequently will have a Botom and a top followed by other elements
		num_prenda_random = random.randint(0, len(top)-1)
		dist_prendes_outfit_random[0] = (top[num_prenda_random])

		num_prenda_random = random.randint(0, len(bottom)-1)
		dist_prendes_outfit_random[1] = (bottom[num_prenda_random])
	
		for x in range(2, rand_num - 2):
			num_prenda_random = random.randint(0, len(others)-1)
			dist_prendes_outfit_random[x] = (others[num_prenda_random])


	else:	#if the number of products on an outfit is bigger, we limit the size of the botom and top products
		already_bottom = False
		already_top = False
		already_dresses = random.randint(1,3) > 1
		frequenciaNoTopBottom =  random.randint(1,4) > 1
		for x in range(rand_num):
			
			if(frequenciaNoTopBottom):
				num_prenda_random = random.randint(0, len(list_prendas)-1)
				if list_prendas[num_prenda_random] in top:
					if already_top:
						rand_num += 1
					else:
						dist_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
						already_top = True
				elif list_prendas[num_prenda_random] in bottom:
					if already_bottom:
						rand_num += 1
					else:
						dist_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
						already_bottom = True
				elif list_prendas[num_prenda_random] in dresses:
					if already_dresses:
						rand_num += 1
					else:
						dist_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
						already_dresses = True
				else:
					dist_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
			else:
				num_prenda_random = random.randint(0, len(others)-1)
				dist_prendes_outfit_random[x] = (others[num_prenda_random])
			
	generateAndSave(dist_prendes_outfit_random,i,2) #we save the outfit on class2