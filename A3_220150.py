# -*- coding: utf-8 -*-
"""Untitled25.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PAncdkhN4IOpXCTiyvq17iJ4uMBdkpvp
"""

import pymc as pm
import pandas as pd
import arviz as az

# Load the dataset
data = pd.read_csv('/content/howell.csv', sep=';')

# Filter out subjects younger than 18
data_adult = data[data['age'] >= 18]

# Extract weight and height
weight = data_adult['weight'].values
height = data_adult['height'].values

# Standardize weight and height
weight_mean = weight.mean()
weight_std = weight.std()
height_mean = height.mean()
height_std = height.std()
weight_standardized = (weight - weight_mean) / weight_std
height_standardized = (height - height_mean) / height_std

# Build and sample the model
with pm.Model() as model:
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + beta * weight_standardized
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=height_standardized)

    trace = pm.sample()

# Summarize and plot the results
az.summary(trace)
az.plot_trace(trace)
az.plot_posterior(trace)

import numpy as np

# New weights to predict
new_weights = np.array([45.73, 65.8, 54.2, 32.59])

# Standardize new weights
new_weights_standardized = (new_weights - weight_mean) / weight_std

# Ensure new weights are in the correct shape for pymc
new_weights_standardized = new_weights_standardized[:, np.newaxis]

# Build and sample the model with new weights
with model:
    pm.MutableData('weight_standardized', new_weights_standardized)
    mu = alpha + beta * new_weights_standardized
    y_pred = pm.Normal('y_pred', mu=mu, sigma=sigma, shape=new_weights_standardized.shape)

    posterior_predictive = pm.sample_posterior_predictive(trace)

# Extract predictions and HDIs
predictions = az.summary(posterior_predictive)
print(predictions)

# Load a dataset (example using the iris dataset)
from sklearn.datasets import load_iris

# Load the dataset
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target

# Simple linear regression: predict petal length from petal width
petal_width = df['petal width (cm)'].values
petal_length = df['petal length (cm)'].values

# Standardize the data
petal_width_mean = petal_width.mean()
petal_width_std = petal_width.std()
petal_length_mean = petal_length.mean()
petal_length_std = petal_length.std()
petal_width_standardized = (petal_width - petal_width_mean) / petal_width_std
petal_length_standardized = (petal_length - petal_length_mean) / petal_length_std

# Build and sample the model
with pm.Model() as iris_model:
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)

    mu = alpha + beta * petal_width_standardized
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=petal_length_standardized)

    iris_trace = pm.sample()

# Summarize and plot the results
az.summary(iris_trace)
az.plot_trace(iris_trace)
az.plot_posterior(iris_trace)
az.plot_pair(iris_trace, var_names=['alpha', 'beta'], kind='kde')