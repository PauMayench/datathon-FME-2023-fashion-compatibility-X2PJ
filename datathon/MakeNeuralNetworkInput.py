import cv2
import os
import numpy as np
import random

from classes import Prenda, Outfit
from obtenirDades import get_dicts


def make_img_input(list_prendas, outfit_id, num_class):

	x_img = 239
	y_img = 334

	img_final = np.zeros(( y_img*3, x_img*5, 3), dtype=np.uint8)

	count = 0

	for p in list_prendas:
		path_img_prenda = p.des_filename

		path_img_prenda = os.path.join(os.getcwd(), "datathon", path_img_prenda)

		img_prenda = cv2.imread(path_img_prenda)


		img_final[0+int(count/5)*y_img:y_img+int(count/5)*y_img, count%5*x_img:x_img+count%5*x_img] = img_prenda

		count += 1

	cv2.imwrite(os.path.join(os.getcwd(), "class"+str(num_class), str(outfit_id)+".jpg"), img_final)



dict_prendas, dict_otufits = get_dicts()

path_images = os.path.join(os.getcwd(), "datathon", "datathon", "images")

# per cada outift
for outfit_key in dict_otufits:
	break # ja estan fets no fa falta repetirho	
	dict_otufits[outfit_key].prendas

	list_prendas_outfit = list(dict_otufits[outfit_key].prendas.values())

	make_img_input(list_prendas_outfit, dict_otufits[outfit_key].cod_outfit, 2)


list_prendas = list(dict_prendas.values())


# fer tants outfits randoms com outfits reals hi hagin
for i in range(len(dict_otufits)):
	list_prendes_outfit_random = []

	for x in range(random.randint(2, 15)):
		num_prenda_random = random.randint(0, len(list_prendas)-1)

		list_prendes_outfit_random.append(list_prendas[num_prenda_random])

	make_img_input(list_prendes_outfit_random, i, 2)