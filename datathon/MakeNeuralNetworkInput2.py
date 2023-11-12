import cv2
import os
import numpy as np
import random

from classes import Prenda, Outfit
from obtenirDades import obtenirDades
from mixImage import cropClassifyImages, mixImage


def generarIguardar(dict_prendas, outfitId ,classId):
	cropped_classified_images = cropClassifyImages(dict_prendas)
	imatgeFinal = mixImage(cropped_classified_images)
	imatgeFinal = cv2.resize(imatgeFinal,(int(imatgeFinal.shape[1]/2), int(imatgeFinal.shape[0]/2)))
	cv2.imwrite(os.path.join(os.getcwd(), "class"+str(classId), str(outfitId)+".jpg"), imatgeFinal)


def filtrar_prendas(list_prendas):
	top = []
	bottom = []
	dresses = []
	others = []
	for prenda in list_prendas:
		if prenda.des_product_category == "Tops":
			top.append(prenda)
		elif prenda.des_product_category == "Bottoms":
			bottom.append(prenda)
		elif prenda.des_product_category == "Dresses, jumpsuits and Complete set":
			bottom.append(prenda)
		else:
			others.append(prenda)

		
	return top, bottom, dresses, others

dict_otufits, dict_prendas = obtenirDades()

for outfit in dict_otufits.values():
	prendas = outfit.prendas
	outfitId = outfit.cod_outfit
	generarIguardar(prendas, outfitId, 1)




list_prendas = list(dict_prendas.values())

top, bottom, dresses, others = filtrar_prendas(list_prendas)


# fer tants outfits randoms com outfits reals hi hagin
for i in range(len(dict_otufits)):
	dist_prendes_outfit_random = {}

	rand_num = random.randint(2, 10)

	if rand_num > 8 or rand_num == 2:
		rand_num = random.randint(2, 10)

	if rand_num <= 5 and random.randint(1, 4) != 1:
		# top bottom accs
		num_prenda_random = random.randint(0, len(top)-1)
		dist_prendes_outfit_random[0] = (top[num_prenda_random])

		num_prenda_random = random.randint(0, len(bottom)-1)
		dist_prendes_outfit_random[1] = (bottom[num_prenda_random])
	
		for x in range(2, rand_num - 2):
			num_prenda_random = random.randint(0, len(others)-1)
			dist_prendes_outfit_random[x] = (others[num_prenda_random])


	else:
		#only accs
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
			
			

	
	generarIguardar(dist_prendes_outfit_random,i,2)