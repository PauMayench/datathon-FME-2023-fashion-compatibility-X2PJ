# TensorFlow and other libraries import
import tensorflow as tf
import numpy as np
import time as t
import os
import cv2


MAX_SAMPLES = 10000 # change this variable to 4000 or 2000

''' This script creates and trains a convolutional neural network using TensorFlow. 
 It processes image data from two categories, trains the model, and then saves it.
'''

# Define the categories for classification
categories = ['class1', 'class2'] # These represent the folders containing the dataset.

# Set up path and data structures for storing images and labels
PATH = os.getcwd()
train_x = [] # List to store training images
train_y = [] # List to store corresponding labels for training images
test_x = [] # List to store testing images
test_y = [] # List to store corresponding labels for testing images

# Define the proportion of data to be used for testing
percentage_testing = 0.05

# Set a limit on the number of samples to be processed
max_samples = MAX_SAMPLES

# Load and process images from each category
for categ in categories:
    nou_path = os.path.join(PATH, categ)
    count = 0
    for path_imatge in os.listdir(nou_path):
        if (max_samples == 0):
            max_samples = MAX_SAMPLES
            break

        max_samples -= 1

        # Read and resize the image
        img = cv2.imread(os.path.join(PATH, categ, path_imatge))
        resizeFact = 2.5
        img = cv2.resize(img, (int(img.shape[1]/resizeFact), int(img.shape[0]/resizeFact)))

        # Split data into training and testing sets
        count += 1
        if (count % (1/percentage_testing) == 0):
            count = 0
            test_x.append(img)
            test_y.append(0 if categ == categories[0] else 1)
        else:
            train_x.append(img)
            train_y.append(0 if categ == categories[0] else 1)

# Convert lists to NumPy arrays for processing
train_x = np.asarray(train_x)
train_y = np.asarray(train_y)
test_x = np.asarray(test_x)
test_y = np.asarray(test_y)

# Define the Convolutional Neural Network model
model = tf.keras.models.Sequential([ 
    tf.keras.layers.Conv2D(64, (5,5), activation="relu", input_shape=(train_x[0].shape), padding='same'),
    tf.keras.layers.MaxPooling2D((3, 3)),
    tf.keras.layers.Conv2D(32, (5,5), activation="relu", padding='same'),
    tf.keras.layers.MaxPooling2D((5, 5)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(2, activation="softmax")
])

# Display model summary
model.summary()
t.sleep(3)

# Compile and train the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(train_x, train_y, epochs=2, batch_size=128, verbose=1, shuffle=True)

# Save the trained model
model.save('model_tensorflow')

# Evaluate the model using the test dataset
print("TRAINING FINISHED, STARTING TEST:")
model.evaluate(test_x, test_y, verbose=2)
