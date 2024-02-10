# -*- coding: utf-8 -*-
"""Vasilescu_Andreea_512.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o7m-8wrXX8ITKIk1e0YMvkgG9f5DYU8h
"""

from google.colab import drive
drive.mount('/content/gdrive')

! ls -s /content/gdrive/MyDrive/smile_non_smile.zip

!unzip "/content/gdrive/MyDrive/smile_non_smile.zip" -d "/content/gdrive/MyDrive/PML2024"

import os
import numpy as np
import pandas as pd
import torch
import matplotlib as plt
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input

smile_path = "/content/gdrive/MyDrive/PML2024/smile"
non_smile_path = "/content/gdrive/MyDrive/PML2024/non_smile"
test_path = "/content/gdrive/MyDrive/PML2024/test"

smile_df = pd.DataFrame(columns=['Image', 'Path'])
non_smile_df = pd.DataFrame(columns=['Image', 'Path'])
test_df = pd.DataFrame(columns = ['Path', 'Path'])

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img = img_to_array(img)
    img = preprocess_input(img)
    return img

def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(120, 120))
    img = img_to_array(img)
    img = preprocess_input(img)
    return img

smile_images_folder = "/content/gdrive/MyDrive/PML2024/smile"
for image_file in os.listdir(smile_images_folder):
    image_path = os.path.join(smile_images_folder, image_file)
    img_data = load_and_preprocess_image(image_path)
    smile_df = smile_df.append({'Image': img_data, 'Path': image_path}, ignore_index=True)

non_smile_images_folder = "/content/gdrive/MyDrive/PML2024/non_smile"
for image_file in os.listdir(non_smile_images_folder):
    image_path = os.path.join(non_smile_images_folder, image_file)
    img_data = load_and_preprocess_image(image_path)
    non_smile_df = non_smile_df.append({'Image': img_data, 'Path': image_path}, ignore_index=True)

test_folder = "/content/gdrive/MyDrive/PML2024/test"
for image_file in os.listdir(test_folder):
    image_path = os.path.join(test_folder, image_file)
    img_data = load_and_preprocess_image(image_path)
    non_smile_df = non_smile_df.append({'Image': img_data, 'Path': image_path}, ignore_index=True)

smile_df

chosen_image_index = 1
chosen_image = smile_df.loc[chosen_image_index, 'Image']
chosen_image_path = smile_df.loc[chosen_image_index, 'Path']

plt.imshow(chosen_image)
plt.title(f"Smile image: {chosen_image_path}")
plt.axis('off')s
plt.show()

image = Image.open("/content/gdrive/MyDrive/PML2024/smile/James_Jones_0001.jpg")
plt.imshow(image)

def load_and_preprocess_images(image_folder):
    images = []
    for image_file in os.listdir(image_folder):
        img = load_img(os.path.join(image_folder, image_file), target_size=(224, 224))
        img = img_to_array(img)
        img = preprocess_input(img)
        images.append(img)
    return images

train_smile_images = load_and_preprocess_images(smile_path)
train_non_smile_images = load_and_preprocess_images(non_smile_path)

all_images = np.vstack((train_smile_images, train_non_smile_images))

"""# Agglomerative clustering

### 1st test with agglomerative
"""

# Combine images and calculate features
all_images = np.vstack((train_smile_images, train_non_smile_images))

# 1st try

# Calculate pairwise distances
distances = pairwise_distances(all_images.reshape(len(all_images), -1), metric="euclidean")

num_clusters = 2  # Number of clusters (smile and nonsmile)
agg_clustering = AgglomerativeClustering(n_clusters=num_clusters, affinity='precomputed', linkage='average')
cluster_labels = agg_clustering.fit_predict(distances)

print("Cluster labels:", cluster_labels)

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances
from scipy.cluster.hierarchy import dendrogram, linkage


linkage_matrix = linkage(distances, method='average')
plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix, labels=cluster_labels, leaf_rotation=0, leaf_font_size=12)
plt.xlabel('Image Index')
plt.ylabel('Distance')
plt.title('Agglomerative Clustering Dendrogram')
plt.show()

"""### second test with agglomerative"""

# 2nd try
num_clusters = 2
agg_clustering = AgglomerativeClustering(n_clusters=num_clusters, affinity='precomputed', linkage='complete')
cluster_labels = agg_clustering.fit_predict(distances)

print("Cluster labels:", cluster_labels)

linkage_matrix = linkage(distances, method='complete')

plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix, labels=cluster_labels, leaf_rotation=0, leaf_font_size=12)
plt.xlabel('2 clusters; precomputed affinity; complete linkage')
plt.ylabel('Distance')
plt.title('Agglomerative Clustering Dendrogram')
plt.show()

"""### 3rd try


"""

# 3rd try

num_clusters = 2
agg_clustering = AgglomerativeClustering(n_clusters=num_clusters, affinity='precomputed', linkage='complete')
cluster_labels = agg_clustering.fit_predict(distances)

print("Cluster labels:", cluster_labels)

# Convert the distances matrix to condensed form
condensed_distances = squareform(distances)

# Create linkage matrix using the condensed form
linkage_matrix = linkage(condensed_distances, method='complete')

# Plot dendrogram
plt.figure(figsize=(10, 5))
dendrogram(linkage_matrix, labels=cluster_labels, leaf_rotation=0, leaf_font_size=12)
plt.xlabel('Image Index')
plt.ylabel('Distance')
plt.title('Agglomerative Clustering Dendrogram')
plt.show()

"""# Isolation Forest"""

# Some imports

import os
import pandas as pd
from sklearn.ensemble import IsolationForest

"""# Isolation Forest - working"""

from sklearn.ensemble import IsolationForest

clf = IsolationForest(contamination=0.1)
clf.fit(all_images.reshape(len(all_images), -1))

anomaly_scores = clf.score_samples(all_images.reshape(len(all_images), -1))

anomaly_threshold = -0.5

categorized_images = ["Smile" if score > anomaly_threshold else "Non_smile" for score in anomaly_scores]
print("Categorized images:", categorized_images)

# Predict anomaly scores
anomaly_scores = clf.score_samples(all_images.reshape(len(all_images), -1))

# Plot histogram of anomaly scores
plt.hist(anomaly_scores, bins=50, density=True, alpha=0.7)
plt.xlabel('Anomaly Score')
plt.ylabel('Density')
plt.title('Anomaly Score Histogram')
plt.show()

for i in range(len(categorized_images)):
  if categorized_images[i] == "Non_smile":
    print (i)

plt.figure(figsize=(12, 6))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    image = all_images[i]
    plt.imshow(image)
    plt.axis('off')

plt.show()

"""## GridSearch for Isolation Forest"""

from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

param_grid = {
    'contamination': [0.05, 0.1, 0.15, 0.2],
    'max_samples': ['auto', 100, 200, 500],
    'n_estimators': [50, 100, 200, 500]
}

for contamination in param_grid['contamination']:
    for max_samples in param_grid['max_samples']:
        for n_estimators in param_grid['n_estimators']:
            clf = IsolationForest(contamination=contamination, max_samples=max_samples, n_estimators=n_estimators)

            clf.fit(all_images.reshape(len(all_images), -1))

            anomaly_scores = clf.score_samples(all_images.reshape(len(all_images), -1))

            plt.hist(anomaly_scores, bins=50, density=True, alpha=0.7)
            plt.xlabel('Anomaly Score')
            plt.ylabel('Density')
            plt.title(f'Anomaly Score Histogram (contamination={contamination}, max_samples={max_samples}, n_estimators={n_estimators})')
            plt.show()

            anomaly_threshold = -0.5
            categorized_images = ["Smile" if score > anomaly_threshold else "Non_smile" for score in anomaly_scores]
            print("Categorized images:", categorized_images)

from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

param_grid = {
    'contamination': [0.05, 0.1, 0.15, 0.2],
    'max_samples': ['auto', 100, 200, 500],
    'n_estimators': [50, 100, 200, 500]
}

fig, axs = plt.subplots(3, 3, figsize=(15, 15))

for i, contamination in enumerate(param_grid['contamination']):
    for j, max_samples in enumerate(param_grid['max_samples']):
        for k, n_estimators in enumerate(param_grid['n_estimators']):
            clf = IsolationForest(contamination=contamination, max_samples=max_samples, n_estimators=n_estimators)

            clf.fit(all_images.reshape(len(all_images), -1))

            anomaly_scores = clf.score_samples(all_images.reshape(len(all_images), -1))

            axs[i, j].hist(anomaly_scores, bins=50, density=True, alpha=0.7)
            axs[i, j].set_title(f'Contam={contamination}, Samples={max_samples}, Estimators={n_estimators}')
            axs[i, j].set_xlabel('Anomaly Score')
            axs[i, j].set_ylabel('Density')

            anomaly_threshold = -0.5
            categorized_images = ["Smile" if score > anomaly_threshold else "Non_smile" for score in anomaly_scores]
            print(f"Results for (contamination={contamination}, max_samples={max_samples}, n_estimators={n_estimators}): {categorized_images}")

plt.tight_layout()
plt.show()

"""tetst2"""

from sklearn.ensemble import IsolationForest

clf = IsolationForest(contamination=0.5)
clf.fit(all_images.reshape(len(all_images), -1))

anomaly_scores = clf.score_samples(all_images.reshape(len(all_images), -1))

anomaly_threshold = -0.5

categorized_images = ["Smile" if score > anomaly_threshold else "Non_smile" for score in anomaly_scores]
print("Categorized images:", categorized_images)

plt.figure(figsize=(12, 6))
for i in range(5):
    plt.subplot(2, 5, i + 1)
    image = all_images[i]
    plt.imshow(image)
    plt.axis('off')

plt.show()

"""# BRICH"""

import pandas as pd
pd.set_option('display.max_rows', None)
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from sklearn.datasets import make_blobs
from sklearn.cluster import Birch

def load_and_preprocess_images(image_folder):
    images = []
    for image_file in os.listdir(image_folder):
        img = load_img(os.path.join(image_folder, image_file), target_size=(224, 224))
        img = img_to_array(img)
        img = preprocess_input(img)
        # Flatten the image
        img = np.ravel(img)
        images.append(img)
    return images

train_smile_images = np.array(load_and_preprocess_images(smile_path))
train_non_smile_images = np.array(load_and_preprocess_images(non_smile_path))
all_images = np.vstack((train_smile_images, train_non_smile_images))

"""2"""

# Generating 600 samples using make_blobs
# centers = n of distinct clusters
# cluster_std = small value -> tighter clusters, large value = spread clusters

from sklearn.datasets import make_blobs
from sklearn.cluster import Birch
import matplotlib.pyplot as plt

dataset, clusters = make_blobs(n_samples=600, centers=2, cluster_std=0.75)

# Number of clusters set to None, so that the algorithm can automatically determine the number of clusters
# Threshold: smaller value - fewer larger clusters; larger - less sensitive, small clusters
model = Birch(branching_factor=20, n_clusters=None, threshold=1.5)

# Fit the model on the generated dataset
model.fit(dataset)

# Predict using the same data
pred = model.predict(dataset)

# Use unique labels for each cluster for plotting
unique_labels = set(pred)

# Creating a scatter plot with unique labels
for label in unique_labels:
    cluster_points = dataset[pred == label]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {label}')

plt.legend()
plt.show()

"""Your session crashed after using all available RAM. If you are interested in access to high-RAM runtimes - COLLAB

2
"""

from sklearn.datasets import make_blobs
from sklearn.cluster import Birch
import matplotlib.pyplot as plt

dataset, clusters = make_blobs(n_samples=1200, centers=2, cluster_std=0.75)

model = Birch(branching_factor=20, n_clusters=None, threshold=1.5)

model.fit(dataset)

pred = model.predict(dataset)

unique_labels = set(pred)

for label in unique_labels:
    cluster_points = dataset[pred == label]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {label}')

plt.legend()
plt.show()

pred =

def load_and_preprocess_images_for_prediction(image_folder):
    images = []
    for image_file in os.listdir(image_folder):
        img = load_img(os.path.join(image_folder, image_file), target_size=(224, 224))
        img = img_to_array(img)
        img = preprocess_input(img)
        img = np.ravel(img)
        images.append(img)
    return images

test_images = np.array(load_and_preprocess_images_for_prediction(test_folder))

# Predict the test data
pred = model.predict(test_images)

# Creating a scatter plot
plt.scatter(test_images[:, 0], test_images[:, 1], c=pred, cmap='rainbow', alpha=0.7, edgecolors='b')
plt.show()