import pandas as pd
from classes import Product, Outfit
import cv2
import numpy as np


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

    
