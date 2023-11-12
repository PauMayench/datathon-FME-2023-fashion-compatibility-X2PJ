import customtkinter as ctk
import numpy as np
from PIL import Image
import random
import os
import cv2
import tensorflow as tf
from utils import outfitImage, obtenirDades, generateListRandomOutfits, transformDict


def get_random_good_outfit(model, dict_prendas):
	list_prendas = list(dict_prendas.values())
	list_dicts_products = []

	inputs_nn = []

	# generar outfits randoms
	list_dicts_products = generateListRandomOutfits(20, list_prendas)
	for i in range(len(list_dicts_products)):
		img = outfitImage(list_dicts_products[i])
		img = cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2)))
		img = cv2.resize(img, (int(img.shape[1]/2.5), int(img.shape[0]/2.5)))
		inputs_nn.append(img) #canviar a entradad dict
	#cv2.imshow("test", list_outfits[i])
	#cv2.waitKey(0)

	# predir si son bons o dolents	
	inputs_nn = tf.data.Dataset.from_tensor_slices(inputs_nn).batch(1)
	print("acaba de tractar input")
	r = list(model.predict(inputs_nn, verbose = 0))


	for i in range(len(r)):
		r[i] = np.argmax(r[i])

		if r[i] == 0: # si es resposta bona
			return list_dicts_products[i]

	return get_random_good_outfit(model, dict_prendas)



def get_random_outfit():
	dict_outfits, dict_prendas  = obtenirDades()

	list_totes_prendas = list(dict_prendas.values())

	product_list = []

	for i in range(random.randint(2, 10)):
		product_list.append(list_totes_prendas[random.randint(1, len(list_totes_prendas))])

	return product_list


def get_product_image(nom_producte):
	path_img = os.path.join(os.getcwd(), nom_producte)

	return cv2.imread(path_img)


def processar_imatge_per_CTK(img, ampl): # Passa d'imatge normal (per exemple cv2) a una versio compatible amb CTKinter. Necessita de input una imatge i la amplada de la finestra
	mides = img.shape

	img = Image.fromarray(img)
	img = ctk.CTkImage(img, size=(ampl, mides[0]/mides[1]*ampl))

	return img

def submitGenerarOutfit():
	global imatges
	global model
	global labels
	global dict_prendas

	rand_num = random.randint(2, 10)


	dict_products_outfit = get_random_good_outfit(model, dict_prendas)
	list_products_outfit = list(dict_products_outfit.values())

	for i in range(10):

		nom_producte = ""

		if i < len(list_products_outfit):
			nom_producte = list_products_outfit[i].des_filename
			img = get_product_image(nom_producte)
			nom_producte = list_products_outfit[i].cod_modelo_color
			img = processar_imatge_per_CTK(img, 100)

		else:
			img = np.full((334,239), 43, np.uint8)
			img = processar_imatge_per_CTK(img, 100)
		
		labels[i].configure(text=nom_producte)
		imatges[i].configure(image=img)


def saveOutfit():
	global labels

	for i in labels:
		text = i.cget("text")
		if text != "":
			print(text)



model = tf.keras.models.load_model("model_tensorflow")

_, dict_prendas = obtenirDades() 

app = ctk.CTk()
app.title("OUTFIT GENERATOR")
app.geometry("740x630")

app.minsize(740,630)
app.maxsize(740,630)

frame_fotos_productes = ctk.CTkFrame(master = app, width=1920, height=1080)
frame_fotos_productes.grid(column=0, row=0, padx= 20, pady= 20)


imatges = []
labels = []
for i in range(10):

	if i < 7:
		img = np.full((334,239), 255, np.uint8)
		img = processar_imatge_per_CTK(img, 100)
		labels.append(ctk.CTkLabel(frame_fotos_productes, text = "test-ini"))

	else:
		img = np.full((334,239), 43, np.uint8)
		img = processar_imatge_per_CTK(img, 100)
		labels.append(ctk.CTkLabel(frame_fotos_productes, text = ""))

	imatges.append(ctk.CTkLabel(frame_fotos_productes, image=img, text=""))
	imatges[i].grid(column=i%5, row = int(i/5)*2, padx=20, pady=10)

	labels[i].grid(column=i%5, row = int(i/5)*2+1, padx=20, pady=10)

boto_generar_outfit = ctk.CTkButton(app, text = "crear outfit", command=submitGenerarOutfit)
boto_generar_outfit.grid(column=0, row=1, padx= 20, pady= 20)

boto_save_outfit = ctk.CTkButton(app, text = "guardar outfit", command=saveOutfit)
boto_save_outfit.grid(column=0, row=2, padx= 20, pady= 20)

app.mainloop()