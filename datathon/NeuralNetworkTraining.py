import tensorflow as tf
import numpy as np
import time as t
import os
import cv2


'''
this python code creates and trains a convolutional model, with the input data and stores the model on model_tensorflow

'''

categories = ['class1', 'class2'] # these are the two folders where we have the input of the model

PATH = os.getcwd()

train_x = [] # arrays of images
train_y = [] # array of the images' labels

test_x = [] # arrays of images
test_y = [] # array of the images' labels

percentage_testing = 0.05 # percentage of the sample images that will be used only for testing

max_samples_ini = 40000 #we put a bug number so it will do all of the tests, if you run with some problems like filling up the ram, you can pitch dowwn this value, it will also reduce the training data
max_samples = max_samples_ini

# Save images from each category (class1 and class2)
for categ in categories:
    nou_path = os.path.join(PATH, categ)
    count = 0
    for path_imatge in os.listdir(nou_path):

        if (max_samples == 0):
            max_samples = max_samples_ini
            break

        max_samples -= 1

        img = cv2.imread(os.path.join(PATH, categ, path_imatge))

        resizeFact = 2.5    # we also can reduce or increment the size of the image, the higher this value, the more we reduce the sizze of each image
        img = cv2.resize(img, (int(img.shape[1]/resizeFact), int(img.shape[0]/resizeFact)))
       
        #cv2.imshow("hehe", img)
        #cv2.waitKey(0)

        count += 1

        if (count % (1/percentage_testing) == 0):
            count = 0
            test_x.append(img)
            if (categ == categories[0]):
                test_y.append(0)
            else:
                test_y.append(1)

        else:
            train_x.append(img)
            if (categ == categories[0]):
                train_y.append(0)
            else:
                train_y.append(1)


print("TRAIN SAMPLES: ", len(train_x))
print("TEST SAMPLES: ", len(test_x))


train_x = np.asarray(train_x)
train_y = np.asarray(train_y)

test_x = np.asarray(test_x)
test_y = np.asarray(test_y)


# INPUT: Matriu gran amb fotos de les prendes
#print(train_x[0].shape)

#The model declaration
model = tf.keras.models.Sequential([ 
    tf.keras.layers.Conv2D(64, (5,5), activation = "relu", input_shape=(train_x[0].shape), padding='same'),
    tf.keras.layers.MaxPooling2D((3, 3)),
    tf.keras.layers.Conv2D(32, (5,5), activation = "relu", padding='same'),
    tf.keras.layers.MaxPooling2D((5, 5)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation = "relu"),
    tf.keras.layers.Dense(32, activation = "relu"),
    tf.keras.layers.Dense(2, activation = "softmax")
    ])

model.summary()

t.sleep(3) # so we can read the output

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


model.fit(train_x, train_y, epochs=2, batch_size=128, verbose=1, shuffle=True)

model.save('model_tensorflow') # The model is saved so that it can be loaded with the function: tf.keras.models.load_model('/tmp/model')

print("TRAINING FINISHED, STARTING TEST:")

model.evaluate(test_x, test_y, verbose=2)