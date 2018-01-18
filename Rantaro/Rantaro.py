import numpy as np
from sklearn import preprocessing

input_data = np.array([[5.1, -2.9, 3.3],
                       [-1.2, 7.8, -6.1],
                       [3.9, 0.4, 2.1],
                       [7.3, -9.9, -4.5]])

# Transforms the data from numerical to boolean using binarization
# All the values above 2.1 threshold become 1. The remaining values become 0.
def Print_binarized_data():
    data_binarized = preprocessing.Binarizer(threshold=2.1).transform(input_data)
    print("\nBinarized data:\n", data_binarized)

def Print_mean_standard_dev():
    # Print mean and standard deviation
    print("\nData set BEFORE:")
    print("Mean =", input_data.mean(axis=0))
    # The .std operator will return the standard deviation of a data set
    print("Std deviation =", input_data.std(axis=0))

# Remove the mean to remove bias from the features in our feature vector
data_scaled = preprocessing.scale(input_data)

def Print_scaled_mean_dev():
    print("\nAFTER:")
    print("Mean =", data_scaled.mean(axis=0))
    print("Std deviation =", data_scaled.std(axis=0))

# Min max scaling (to avoid artificially large or small features)
data_scaler_minmax = preprocessing.MinMaxScaler(feature_range=(0, 1))
data_scaled_minmax = data_scaler_minmax.fit_transform(input_data)

def Print_scaled_minmax():
    # Each row is scaled so that the maximum value is 1 and all the other values
    # are relative to this value
    print("\nMin max scaled data:\n", data_scaled_minmax)
    
# Normalise data using L1 Normalisation, which refers to 'Least Absolute Deviations'
# this works by making sure that the sum of absolute values is 1 in each row.
# L1 is robust as it is resistant to outliers in the data.
data_normalised_l1 = preprocessing.normalize(input_data, norm='l1')
data_normalised_l2 = preprocessing.normalize(input_data, norm='l2')

def Print_normalised_data():
    print("\nL1 Normalised data:\n", data_normalised_l1)
    print("\nL2 Normalised data:\n", data_normalised_l2)