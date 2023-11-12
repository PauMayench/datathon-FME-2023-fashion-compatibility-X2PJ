#represents a product with all its atributes
class Product:
    def __init__(self, modelo_color, color_code, color_specification_esp, agrup_color_eng, sex, age, line, fabric, product_category, product_aggregated_family, product_family, product_type, filename):
        self.cod_modelo_color = modelo_color
        self.cod_color_code = color_code
        self.des_color_specification_esp = color_specification_esp
        self.des_agrup_color_eng = agrup_color_eng
        self.des_sex = sex
        self.des_age = age
        self.des_line = line
        self.des_fabric = fabric
        self.des_product_category = product_category 
        self.des_product_aggregated_family = product_aggregated_family
        self.des_product_family = product_family
        self.des_product_type = product_type
        self.des_filename = filename

#represents an outfit, with products as a dictionary having cod_modelo_color as key and the product as value
class Outfit:
    def __init__(self, outfitId):
        self.cod_outfit = outfitId
        self.products = {}