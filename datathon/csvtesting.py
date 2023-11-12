import pandas as pd
import pprint
import cv2


base_path = "dataset/"
product_data = pd.read_csv(base_path+"product_data.csv", sep=',', header=0)
outfit_data = pd.read_csv(base_path+"outfit_data.csv", sep=',', header=0)


category_list = []
aggregated_family_list = []
family_list = []
general_list = []

count = 0
for index, row in product_data.iterrows():
    
        
    if row['des_product_category'] == "Home":
        im = cv2.imread( row['des_filename'])
        cv2.imshow("hehe", im)
        cv2.waitKey(0)
        count += 1

print("count =", count)
print(general_list)

'''
keys = [
"57074037-98"]

model = []
for index, row in product_data.iterrows():
    
    if row['cod_modelo_color'] in keys:
        model.append(row['des_filename'])
        '''

#pprint.pprint(model)