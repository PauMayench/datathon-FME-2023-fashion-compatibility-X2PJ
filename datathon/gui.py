import customtkinter as ctk
import numpy as np
from PIL import Image
import random
import os
import cv2
import tensorflow as tf
from pprint import pprint
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
		inputs_nn.append(img)


	# predir si son bons o dolents	
	inputs_nn = tf.data.Dataset.from_tensor_slices(inputs_nn).batch(1)
	r = list(model.predict(inputs_nn, verbose = 0))

	for i in range(len(r)):
		if (r[i][0] > 0.8):
			r[i] = 0
		else:
			r[i] = 1


		if r[i] == 0: # si es resposta bona
			return list_dicts_products[i]

	return get_random_good_outfit(model, dict_prendas)


def get_product_image(nom_producte):
	path_img = os.path.join(os.getcwd(), nom_producte)

	return cv2.imread(path_img)


def processar_imatge_per_CTK(img, ampl): # Passa d'imatge normal (per exemple cv2) a una versio compatible amb CTKinter. Necessita de input una imatge i la amplada de la finestra
	mides = img.shape

	img = Image.fromarray(img)
	img = ctk.CTkImage(img, size=(ampl, mides[0]/mides[1]*ampl))

	return img

def submitGenerarOutfit():
	global widgets_imatges
	global imatges
	global model
	global labels
	global dict_prendas

	rand_num = random.randint(2, 10)

	imatges = []

	dict_products_outfit = get_random_good_outfit(model, dict_prendas)
	list_products_outfit = list(dict_products_outfit.values())

	for i in range(10):

		nom_producte = ""

		if i < len(list_products_outfit):
			nom_producte = list_products_outfit[i].des_filename
			img = get_product_image(nom_producte)
			nom_producte = list_products_outfit[i].cod_modelo_color
			imatges.append(img)
			img = processar_imatge_per_CTK(img, 100)

		else:
			img = np.full((334,239), 43, np.uint8)
			img = processar_imatge_per_CTK(img, 100)
		
		labels[i].configure(text=nom_producte)
		widgets_imatges[i].configure(image=img)


def saveOutfit():
	global labels
	global imatges

	arxius = os.listdir(os.getcwd())

	generar_carpeta = True
	for a in arxius:
		if a == "generated_outfits":
			generar_carpeta = False

	if generar_carpeta:
		os.mkdir("generated_outfits")

	num = 1

	while True:		
		existeix = False
		for a in os.listdir(os.path.join(os.getcwd(), "generated_outfits")):
			if a == "outfit"+str(num):
				existeix = True
				num += 1
				break
		if not existeix:
			break


	os.mkdir(os.path.join("generated_outfits", "outfit"+str(num)))

	f = open(os.path.join("generated_outfits", "outfit"+str(num), "outfit"+str(num)+".txt"), "w")
	for i in labels:
		text = i.cget("text")
		f.write(text+"\n")

	for i in range(len(imatges)):
		nom_prod = labels[i].cget("text")
		cv2.imwrite(os.path.join("generated_outfits", "outfit"+str(num), nom_prod+".png"), imatges[i])

	f.close()


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
widgets_imatges = []
labels = []
for i in range(10):

	img = np.full((334,239), 43, np.uint8)
	img = processar_imatge_per_CTK(img, 100)
	labels.append(ctk.CTkLabel(frame_fotos_productes, text = ""))

	widgets_imatges.append(ctk.CTkLabel(frame_fotos_productes, image=img, text=""))
	widgets_imatges[i].grid(column=i%5, row = int(i/5)*2, padx=20, pady=10)

	labels[i].grid(column=i%5, row = int(i/5)*2+1, padx=20, pady=10)

boto_generar_outfit = ctk.CTkButton(app, text = "create outfit", command=submitGenerarOutfit)
boto_generar_outfit.grid(column=0, row=1, padx= 20, pady= 20)

boto_save_outfit = ctk.CTkButton(app, text = "save outfit", command=saveOutfit)
boto_save_outfit.grid(column=0, row=2, padx= 20, pady= 20)

app.mainloop()