# UPC Datathon 2023 - Fashion Compatibility Challenge

## Overview
In the Fashion Compatibility Challenge, participants are tasked with creating a model that can generate outfits with compatible fashion products.
We adopted a convolutional neural network approach, where given some outfits on the format of images and metadata we create an image like this, and feed the model with it to train it. 

![Product1](resources/2019_51030857_20.jpg)
![Product1](resources/2019_53003778_OR.jpg)
![Product1](resources/2019_53023716_07.jpg)
![Product1](resources/2019_53023770_04.jpg)
![Product1](resources/2019_57095923_CU.jpg)

===================================================
![Final Outfit](resources/156.jpg)

This model is able to tell, given an outfit, the degree of compatibility between the fashon products 

Then we implemented a gui where you can generate outfits, each time you press the button "generate outfit" it creates 20 random outfits, each of them is given to the trained model and it returns the respective compatibility, if the best one is over a certain threshold we show it to the user, if not, we call the function again.




## Getting Started

### Prerequisites
Before running the code, ensure that you have the following prerequisites installed:
- Python 3.x
- OpenCV library
- NumPy library
- TensorFlow library
- Customtkinter library
- Pillow Library


### Installation
Clone the repository to your local machine:
`git clone https://github.com/PauMayench/datathon-FME-2023-fashion-compatibility-X2PJ.git`

Navigate to the project directory:
`cd datathon-FME-2023-fashion-compatibility-X2PJ`

Install the required Python packages:
`pip install -r requirements.txt`


### Usage
First of all move to the datathon directory with:
`cd datathon`
unzip the folder inside datathon images.zip with:
`unzip datathon/images.zip datathon/images`

Now you can execute the gui with:
`python3 gui.py`

You can train the model by following the steps:

To generate the training samples run:
`python3 MakeNeuralNetworkInput.py`

To train the model on the generated data simply run:
`python3 NeuralNetworkTraining.py`
WARNING: you have to have some free RAM on your laptop on the moment of execution, on our tests we needed at least 12G, if your training fails you can go inside the code and change the variable MAX_SAMPLES to smaller values like 4000 or 2000, the model will be trained with less data


## Data Structure
The dataset consists of images categorized into different classes. The 'class1' directory contains images of 'good' outfits, while 'class2' houses 'bad' outfits generated with certain constraints.

## Model Training
The provided Python script reads image data, preprocesses it, and fits it to a convolutional neural network model. The model is then saved and evaluated against a test set. 

## GUI





## IMPROVEMENTS
We could train the model with some metadata that comes from the products, as we are currently not using. We could also create a better way to generate outfits that we send to train to the model as not good, because the generation is random and it could happend that they are good.



## Acknowledgments
- Thanks to MANGO for providing the expertly curated outfit data.

