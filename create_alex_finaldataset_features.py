# -*- coding: utf-8 -*-
"""Create alex finaldataset features

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1id2fGrIhWfPrLA1DYcLb5SGlUBT6VXKf

# import & mount
"""

import matplotlib
import matplotlib.pyplot as plt  # Most common visualization package that a lot of others are based on

import numpy as np  # Common package for numerical methods
import pandas as pd  # Common package for data storeage/manipulation
import seaborn as sns  # Common package for statistical visualizations
import datetime

# from IPython.display import SVG
# from graphviz import Source

# Import useful packages from sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegressionCV
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# Torch and Time!
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torch.utils.data.sampler import SubsetRandomSampler
import torchvision.transforms as transforms

# Import portion of a package
import scipy.stats as stats
from sklearn.impute import SimpleImputer as Imputer  # Specific function from common machine learning package

from PIL import ImageFile

import torchvision.models
alexnet = torchvision.models.alexnet(pretrained=True)
import os
import multiprocessing


"""# features"""

new_path = os.getcwd()+'\\Alex_Net_Features_FinalDataset'

batch_size = 1
num_workers=1

path = os.getcwd()+'\\FinalDataset'

classes = []
for folder in os.scandir(path):
 classes.append(folder.name)

classes.sort()
print(classes)
print(len(classes))

# define the transforms to be applied to the images
transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])

pics = torchvision.datasets.ImageFolder(path, transform=transform)

# split into training, validation, and testing sets (60,20,20)
train_size = int(0.60 * len(pics))
val_size = int(0.20 * len(pics))
test_size = len(pics) - train_size - val_size
train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(pics, [train_size, val_size, test_size])

# create data loaders for each of the datasets
train_loader_alex = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=True)
val_loader_alex = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=True)
test_loader_alex = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, num_workers=num_workers, shuffle=True)

ImageFile.LOAD_TRUNCATED_IMAGES = True

if not os.path.isdir(new_path):
  os.mkdir(new_path)

trainPath = new_path + '\\train\\'
if not os.path.isdir(trainPath):
  os.mkdir(trainPath)

valPath = new_path + '\\val\\'
if not os.path.isdir(valPath):
  os.mkdir(valPath)

testPath = new_path + '\\test\\'
if not os.path.isdir(testPath):
  os.mkdir(testPath)

if __name__ == '__main__':
  multiprocessing.freeze_support()
  i = 0
  for img, label in train_loader_alex:
      features = alexnet.features(img)
      features_tensor = torch.from_numpy(features.detach().numpy())
      folder_name = trainPath + str(classes[label])
      if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
      torch.save(features_tensor.squeeze(0), folder_name + '\\' + str(i) + '.tensor')
      i += 1
  print("Completed Train")
  i = 0
  for img, label in val_loader_alex:
      features = alexnet.features(img)
      features_tensor = torch.from_numpy(features.detach().numpy())
      folder_name = valPath + str(classes[label])
      if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
      torch.save(features_tensor.squeeze(0), folder_name + '\\' + str(i) + '.tensor')
      i += 1
  print("Completed Val")
  i = 0
  for img, label in test_loader_alex:
      features = alexnet.features(img)
      features_tensor = torch.from_numpy(features.detach().numpy())
      folder_name = testPath + str(classes[label])
      if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
      torch.save(features_tensor.squeeze(0), folder_name + '\\' + str(i) + '.tensor')
      i += 1