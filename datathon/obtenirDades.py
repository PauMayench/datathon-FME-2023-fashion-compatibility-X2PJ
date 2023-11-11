import pandas as pd
from classes import Prenda, Outfit

base_path = "dataset/"
product_data = pd.read_csv(base_path+"product_data.csv", sep=',', header=0)
outfit_data = pd.read_csv(base_path+"outfit_data.csv", sep=',', header=0)

# llista de prendas
prendas = {}

for index, row in product_data.iterrows():
    p = Prenda(
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
    prendas[row['cod_modelo_color']] = p

# llista d'outfits
outfits = {}

for index, row in outfit_data.iterrows():
    clauPrenda = row['cod_modelo_color']
    # comprovem que l'outfit no està inicialitzat, si no ho està l'inicialitzem posant-li el seu codi
    if row['cod_outfit'] not in outfits:
        o = Outfit(row['cod_outfit'])
        outfits[row['cod_outfit']] = o
    outfits[row['cod_outfit']].prendas[clauPrenda] = prendas[clauPrenda] # afegeix la prenda d'aquesta fila al seu outfit

print(outfits)