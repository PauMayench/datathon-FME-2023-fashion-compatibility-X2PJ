import customtkinter as ctk
import numpy as np
from PIL import Image
import random
from obtenirDades import get_dicts
import os
import cv2
import tensorflow as tf
from mixImage import list_prendas_to_input_img


def get_random_good_outfit(model):

	list_outfits = []

	# generar outfits randoms
	for i in range(10):
		list_prendes_outfit = get_random_outfit()
		list_outfits.append(list_prendes_outfit)
		list_outfits[i] = list_prendas_to_input_img(list_outfits[i])
		cv2.imshow("test", list_outfits[i])
		cv2.waitKey(0)

	# predir si son bons o dolents	
	list_outfits = tf.data.Dataset.from_tensor_slices(imatges).batch(1)
	resposta = list(model.predict(imatges, verbose = 0))

	for i in range(len(resposta)):
		r[i] = np.argmax(r[i])

		if r[i] == 0: # si es resposta bona
			return list_outfits

	get_random_good_outfit(model)



def get_random_outfit():
	dict_prendas, dict_outfits = get_dicts()

	list_totes_prendas = list(dict_prendas.values())

	list_prendes_output = []

	for i in range(random.randint(2, 10)):
		list_prendes_output.append(list_totes_prendas[random.randint(1, len(list_totes_prendas))])

	return list_prendes_output


def get_product_image(nom_producte):
	path_img = os.path.join(os.getcwd(), "datathon", nom_producte)

	return cv2.imread(path_img)


def processar_imatge_per_CTK(img, ampl): # Passa d'imatge normal (per exemple cv2) a una versio compatible amb CTKinter. Necessita de input una imatge i la amplada de la finestra
	mides = img.shape

	img = Image.fromarray(img)
	img = ctk.CTkImage(img, size=(ampl, mides[0]/mides[1]*ampl))

	return img

def funcio():
	global imatges
	global model

	rand_num = random.randint(2, 10)


	list_products_outfit = get_random_good_outfit(model)


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


model = tf.keras.models.load_model("model_tensorflow")


app = ctk.CTk()
app.title("OUTFIT GENERATOR")
app.geometry("740x530")

app.minsize(740,530)
app.maxsize(740,530)

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

boto_generar_outfit = ctk.CTkButton(app, text = "crear outfit", command=funcio)
boto_generar_outfit.grid(column=0, row=1, padx= 20, pady= 20)

app.mainloop()