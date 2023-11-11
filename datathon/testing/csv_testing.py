#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


base_path = "/home/dev/Git/Hackatons/datathon-FME-2023-fashion-compatibility-X2PJ/datathon/dataset/"
product_data = pd.read_csv(base_path+"product_data.csv", sep=',', header=0)
outfit_data = pd.read_csv(base_path+"outfit_data.csv", sep=',', header=0)


# In[5]:


product_data.head(3)


# In[6]:


outfit_data.head(3)


# In[27]:


# "outfit_id" = [num_prendas, [prenda1...prendaN]]
n_prendas = {}

for index, row in outfit_data.iterrows():
    outfit_id = row['cod_outfit']
    if outfit_id not in n_prendas:
        n_prendas[outfit_id] = 1
        # n_prendas[outfit_id] = [1, [row['cod_modelo_color']]]
    else:
        n_prendas[outfit_id] += 1
        # n_prendas[outfit_id][0] += 1
        # n_prendas[outfit_id][1].append(row['cod_modelo_color'])


# In[30]:


max_n_prendas = max(n_prendas.values())
max_n_prendas


# In[28]:


max_outfit = max(n_prendas.keys())
max_outfit


# In[38]:


# des_product_category
# des_product_aggregated_familyDecorDecor
# des_product_family
# des_product_type

category_list = []
aggregated_family_list = []
family_list = []
type_list = []

for index, row in product_data.iterrows():
    
    if row['des_product_category'] not in category_list:
        category_list.append(row['des_product_category'])
        
    if row['des_product_aggregated_family'] not in aggregated_family_list:
        aggregated_family_list.append(row['des_product_aggregated_family'])
        
    if row['des_product_family'] not in family_list:
        family_list.append(row['des_product_family'])
        
    if row['des_product_type'] not in type_list:
        type_list.append(row['des_product_type'])


# In[39]:


category_list


# In[40]:


aggregated_family_list


# In[41]:


family_list


# In[46]:


type_list

