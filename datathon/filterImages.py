import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np

def load_and_preprocess_image(img_path, target_size=(224, 224)): #returns the image of the path preprocessed, resized with target_size (the default is 224x224)


    img = image.load_img(img_path, target_size=target_size)

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    img_array = preprocess_input(img_array)

    return img_array


img_path = 'datathon/images/2019_43040692_OR.jpg'
processed_image = load_and_preprocess_image(img_path)
print(processed_image)