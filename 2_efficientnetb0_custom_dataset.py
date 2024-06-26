# -*- coding: utf-8 -*-
"""2-efficientnetB0_Custom_dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1afCDZQoQLOyN5pPxB6oc6LN8xDvRMhOU

# EfficientNet Implementation   - EfficientNet- B0

## Training a Custom  Model from scratch
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

from google.colab import drive
drive.mount('/content/drive')

"""![image.png](attachment:image.png)

# Data Pre Processing
"""

from PIL import Image, ImageEnhance
import os
import numpy as np

def rotate_and_save_image(image_path, output_dir, degrees, folder_name, i):
    with Image.open(image_path) as img:
        rotated_img = img.rotate(degrees, expand=True)
        base_name = os.path.basename(image_path)
        file_name, ext = os.path.splitext(base_name)
        output_file_name = f"{folder_name}_rotated_{i}{ext}"
        output_path = os.path.join(output_dir, output_file_name)
        rotated_img.save(output_path)
        print(f"Saved rotated image to {output_path}")
        return i + 1

def process_images(image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    folder_name = os.path.basename(image_dir)
    i = 1
    for file_name in os.listdir(image_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_dir, file_name)
            for degrees in [90, 180, 270, 360]:
                i = rotate_and_save_image(image_path, output_dir, degrees, folder_name, i)
    return i # Return the final value of i

def adjust_contrast_and_save_image(image_path, output_dir, contrast_factor, folder_name, i):
    with Image.open(image_path) as img:
        # Ensure the image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Create a contrast enhancer
        enhancer = ImageEnhance.Contrast(img)

        # Adjust the contrast
        adjusted_img = enhancer.enhance(contrast_factor)

        # Prepare the output file name
        base_name = os.path.basename(image_path)
        file_name, ext = os.path.splitext(base_name)
        output_file_name = f"{folder_name}_contrast_{i}{ext}"
        output_path = os.path.join(output_dir, output_file_name)

        # Save the adjusted image
        adjusted_img.save(output_path)
        print(f"Saved adjusted image to {output_path}")
        return i + 1

def process_images_with_contrast(image_dir, output_dir, x):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    folder_name = os.path.basename(image_dir)
    i = 1
    for file_name in os.listdir(image_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_dir, file_name)
            for contrast_factor in [0.5, 1.5]:
                i = adjust_contrast_and_save_image(image_path, output_dir, contrast_factor, folder_name, i)

def resize_and_save_image(image_path, output_dir, new_size=(224, 224), folder_name=None, i=1):
    with Image.open(image_path) as img:
        # Ensure the image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize the image
        resized_img = img.resize(new_size) # Defaults to Image.BICUBIC

        # Prepare the output file name
        base_name = os.path.basename(image_path)
        file_name, ext = os.path.splitext(base_name)
        output_file_name = f"{folder_name}_{i}{ext}"
        output_path = os.path.join(output_dir, output_file_name)

        # Save the resized image
        resized_img.save(output_path)
        print(f"Saved resized image to {output_path}")
        return i + 1

def process_images_with_resize(image_dir, output_dir, new_size=(224, 224)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    folder_name = os.path.basename(image_dir)
    i = 1
    for file_name in os.listdir(image_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_dir, file_name)
            i = resize_and_save_image(image_path, output_dir, new_size, folder_name, i)
    return i # Return the final value of i

def add_gaussian_noise(image_dir, output_dir, sigma_values, start_index=1):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    i = start_index
    for file_name in os.listdir(image_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(image_dir, file_name)
            try:
                with Image.open(image_path) as img:
                    img_array = np.array(img)
                    for sigma in sigma_values:
                        noise = np.random.normal(0, sigma, img_array.shape)
                        noisy_img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
                        noisy_img = Image.fromarray(noisy_img_array)

                        base_name, ext = os.path.splitext(file_name)
                        output_file_name = f"{base_name}_noisy_sigma_{sigma}{ext}"
                        output_path = os.path.join(output_dir, output_file_name)

                        noisy_img.save(output_path)
                        print(f"Saved noisy image with sigma {sigma} to {output_path}")
                        i += 1
            except Exception as e:
                print(f"Error adding Gaussian noise to {image_path}: {e}")
    return i

for folder_index in range(1, 7):
    image_dir = f'/content/drive/MyDrive/Dataset Folder/grade{folder_index-1}'
    output_dir = f'/content/drive/MyDrive/Buffer/Grade ({folder_index-1})'
    output_dir1 = f'/content/drive/MyDrive/Pre-processed/Grade ({folder_index-1})'
    image_dir1 = f'/content/drive/MyDrive/Buffer/Grade ({folder_index-1})'
    sigma_values = [20, 30, 40]


    # Process images and get the final value of i
    final_i = process_images(image_dir, output_dir)

    # Use the final value of i as the starting point for process_images_with_contrast
    process_images_with_contrast(image_dir1, output_dir, final_i)

    final_index = add_gaussian_noise(image_dir1, output_dir, sigma_values)

    # Now, process images with resize
    final_i_resize = process_images_with_resize(image_dir1, output_dir1)

import numpy as np
import tensorflow as tf

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

dataset_path = os.listdir('/content/drive/MyDrive/dataset')

print (dataset_path)  #what kinds of classes are in this dataset

print("Types of classes labels found: ", len(dataset_path))

class_labels = []

for item in dataset_path:
 # Get all the file names
 all_classes = os.listdir('/content/drive/MyDrive/dataset' + '/' +item)
 #print(all_classes)

 # Add them to the list
 for room in all_classes:
    class_labels.append((item, str('dataset_path' + '/' +item) + '/' + room))
    #print(class_labels[:5])

# Build a dataframe
df = pd.DataFrame(data=class_labels, columns=['Labels', 'image'])
print(df.head())
print(df.tail())

# Let's check how many samples for each category are present
print("Total number of images in the dataset: ", len(df))

label_count = df['Labels'].value_counts()
print(label_count)

import cv2
path = '/content/drive/MyDrive/dataset/'
dataset_path = os.listdir('/content/drive/MyDrive/dataset')
im_size = 224

images = []
labels = []

for i in dataset_path:
    data_path = path + str(i)
    filenames = [i for i in os.listdir(data_path)]
    for f in filenames:
        img = cv2.imread(data_path + '/' + f)
        img = cv2.resize(img, (im_size, im_size))
        images.append(img)
        labels.append(i)

# Convert lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Normalize pixel values
images = images.astype('float32') / 255.0

from sklearn.preprocessing import LabelEncoder , OneHotEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# One-hot encode labels
ct = ColumnTransformer([('one_hot', OneHotEncoder(), [0])], remainder='passthrough')
Y = ct.fit_transform(encoded_labels.reshape(-1, 1))

# Shuffle the data
images, Y = shuffle(images, Y, random_state=1)

# Split the data into training and testing sets
train_x, test_x, train_y, test_y = train_test_split(images, Y, test_size=0.20, random_state=415)

# Inspect the shapes of the training and testing data
print(f"Train images shape: {train_x.shape}")
print(f"Train labels shape: {train_y.shape}")
print(f"Test images shape: {test_x.shape}")
print(f"Test labels shape: {test_y.shape}")

"""
# EfficientNet Implementation :

"""

from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0

NUM_CLASSES = 1  # Change to 1 for binary classification
IMG_SIZE = 224
size = (IMG_SIZE, IMG_SIZE)

inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

# Using model without transfer learning
outputs = EfficientNetB0(include_top=True, weights=None, classes=NUM_CLASSES)(inputs)

model = tf.keras.Model(inputs, outputs)

# Modify the loss function to binary_crossentropy
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

model.summary()

hist = model.fit(train_x, train_y, epochs=30, verbose=2)

import matplotlib.pyplot as plt


def plot_hist(hist):
    plt.plot(hist.history["accuracy"])
    #plt.plot(hist.history["val_accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    plt.show()


plot_hist(hist)

preds = model.evaluate(test_x, test_y)
print ("Loss = " + str(preds[0]))
print ("Test Accuracy = " + str(preds[1]))

"""# Testing Efficient Model On Unseen data"""

from matplotlib.pyplot import imread
from matplotlib.pyplot import imshow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications.imagenet_utils import preprocess_input



img_path = '/content/drive/MyDrive/dataset/Normal/114.jpg'

#img = image.load_img(img_path, target_size=(224, 224))
#x = img.img_to_array(img)

img = cv2.imread(img_path)
img = cv2.resize(img, (224, 224))

x = np.expand_dims(img, axis=0)
x = preprocess_input(x)

print('Input image shape:', x.shape)

my_image = imread(img_path)
imshow(my_image)

preds=model.predict(x)
preds # probabilities for being in each of the 3 classes

# Cuda and cudnn is installed for this tensorflow version. So we can see GPU is enabled
tf.config.experimental.list_physical_devices()

# Commented out IPython magic to ensure Python compatibility.
# %%timeit -n1 -r1
# with tf.device('/GPU:0'):
#     gpu_performance =model.fit(train_x, train_y, epochs=30, verbose=2)
#     gpu_performance

# Commented out IPython magic to ensure Python compatibility.
# 
# %%timeit -n1 -r1
# with tf.device('/GPU:0'):
#     gpu_performance =model.fit(train_x, train_y, epochs=30, verbose=2)
#     gpu_performance

# CPU completed the training in 7 min 53 Seconds and GPU did that training in 25.6 seconds