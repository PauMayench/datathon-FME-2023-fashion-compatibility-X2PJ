class Prenda:
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

class Outfit:
    def __init__(self, outfit):
        self.cod_outfit = outfit
        self.prendas = dict()

    def addPrenda(self, clau, prenda):
        self.prendas[clau] = Prenda(prenda)
