import pandas as pd
from classes import Product, Outfit
import cv2
import numpy as np
import random

base_path = "dataset/"

# reads csv and returns them as dictionaries of class instances
def obtenirDades():
    product_data = pd.read_csv(base_path+"product_data.csv", sep=',', header=0)
    outfit_data = pd.read_csv(base_path+"outfit_data.csv", sep=',', header=0)
    products = {}
    for index, row in product_data.iterrows():
        p = Product(
            row['cod_modelo_color'], 
            row['cod_color_code'], 
            row['des_color_specification_esp'], 
            row['des_agrup_color_eng'], 
            row['des_sex'], 
            row['des_age'], 
            row['des_line'], 
            row['des_fabric'], 
            row['des_product_category'], 
            row['des_product_aggregated_family'], 
            row['des_product_family'], 
            row['des_product_type'], 
            row['des_filename']
        )
        products[row['cod_modelo_color']] = p

    # llista d'outfits
    outfits = {}

    for index, row in outfit_data.iterrows():
        clauproduct = row['cod_modelo_color']
        # comprovem que l'outfit no està inicialitzat, si no ho està l'inicialitzem posant-li el seu codi
        if row['cod_outfit'] not in outfits:
            o = Outfit(row['cod_outfit'])
            outfits[row['cod_outfit']] = o
        outfits[row['cod_outfit']].products[clauproduct] = products[clauproduct] # afegeix la product d'aquesta fila al seu outfit

    return outfits, products

#recieves a product dictionary, with its id as keys, it returns an image of the outfit    
def outfitImage(products):
    #recieves a  dictionary with categories as keys and product lists as values, it returns an image of the outfit auxiliary function for outfitImage
    def mixImage(cropped_classified_images):
        # Define canvas size
        canvas_width, canvas_height = 239*5, 334*3
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        # Define regions for each category
        #['Bottoms', 'Dresses, jumpsuits and Complete set', 'Tops', 'Accesories, Swim and Intimate', 'Outerwear', 'Beauty', 'Home']

        regions = { #home and beauty where deemed irrelevant to try to improve the performance of the training 
            "Tops": 0,
            "Dresses, jumpsuits and Complete set":3,
            "Bottoms": 5,
            "Accesories, Swim and Intimate":10,
            "Outerwear": 8
        }

        x_img = 239
        y_img = 334

        for category, image_list in cropped_classified_images.items():
            if category in regions:
                try:
                    count = regions[category]
                    for image in image_list:
                        if count >= 15: count = 8
                        canvas[0+int(count/5)*y_img:y_img+int(count/5)*y_img, count%5*x_img:x_img+count%5*x_img] = image
                        count += 1
                except:
                    pass

        return canvas
    cropped_classified_images = {}
    for product in products.values():

        image = cv2.imread(product.des_filename)

        if image is None: #if image is not found, ignore it
            print(f"Image not found: {product.des_filename}")
            continue

        if(product.des_product_category in cropped_classified_images):  # Appends the image to the correspondig dictionary category key
            cropped_classified_images[product.des_product_category].append(image)
        else:
            cropped_classified_images[product.des_product_category] = [image]
        
    return mixImage(cropped_classified_images)
 
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
		elif product.des_product_category == "Beauty" or product.des_product_category == "Home":
			pass
		else:
			others.append(product)
	return top, bottom, dresses, others

#recieves a list of products and returns n lists of products on a list,they are the possible outfits
def generateListRandomOutfits(n, list_prendas):
	top, bottom, dresses, others = productFilter(list_prendas)
	list_dicts_products = []
	for i in range(n):

		dict_prendes_outfit_random = {}

		rand_num = random.randint(2, 10)

		if rand_num > 8 or rand_num == 2:	# this reduces the chances of creating outfits with extreme number of products
			rand_num = random.randint(2, 10)

		if rand_num <= 5 and random.randint(1, 4) != 1: # if the number of products is small, most frequently will have a Botom and a top followed by other elements
			num_prenda_random = random.randint(0, len(top)-1)
			dict_prendes_outfit_random[0] = (top[num_prenda_random])

			num_prenda_random = random.randint(0, len(bottom)-1)
			dict_prendes_outfit_random[1] = (bottom[num_prenda_random])
		
			for x in range(2, rand_num - 2):
				num_prenda_random = random.randint(0, len(others)-1)
				dict_prendes_outfit_random[x] = (others[num_prenda_random])


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
							dict_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
							already_top = True
					elif list_prendas[num_prenda_random] in bottom:
						if already_bottom:
							rand_num += 1
						else:
							dict_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
							already_bottom = True
					elif list_prendas[num_prenda_random] in dresses:
						if already_dresses:
							rand_num += 1
						else:
							dict_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
							already_dresses = True
					else:
						dict_prendes_outfit_random[x] = (list_prendas[num_prenda_random])
				else:
					num_prenda_random = random.randint(0, len(others)-1)
					dict_prendes_outfit_random[x] = (others[num_prenda_random])
					
		list_dicts_products.append(dict_prendes_outfit_random)
		
	return list_dicts_products

def transformDict(list_products):
	d = {}
	for product in list_products:
		d[product.cod_modelo_color] = product

	return d
