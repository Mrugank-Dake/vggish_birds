
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
import matplotlib
from datetime import datetime
import os
import pickle
import calendar


'''
This module provides functions to assist with plotting our data
'''


def plot_multi_class_recalls(recalls, labels, average_accuracy, cm_values, label_type, feat):
    '''
    Plot recall for each class as a result of a multiclass classification task

    Inputs:
        recalls (ndarray): vector of recalls for each class
        labels (ndarray): label corresponding to each class
        average_accuracy (float): balanced average recall across all classes
        label_type (str): type of label used (e.g. 'dataset', 'land-use', 'hour', 'month' etc.)
        feat (str): acoustic feature set used
    '''

    # Convert decimals to percentages
    recalls = recalls * 100
    average_accuracy = average_accuracy * 100

    # Get sensible order for labels
    order = get_label_order(labels,label_type)
    recalls = np.asarray(recalls)
    recalls = recalls[order]
    labels = labels[order]

    bar1 = plt.bar(labels, recalls)
    indexing = 0
    for rect in bar1:
        
        height = rect.get_height()
        #print(rect)
        plt.text(rect.get_x() + rect.get_width()/2.0, height - 5, 'tp = ' + str(round(cm_values[0][indexing])), ha='center', va='bottom')
        plt.text(rect.get_x() + rect.get_width()/2.0, height - 10, 'tn = ' + str(round(cm_values[1][indexing])), ha='center', va='bottom')
        plt.text(rect.get_x() + rect.get_width()/2.0, height - 15, 'fp = ' + str(round(cm_values[2][indexing])), ha='center', va='bottom')
        plt.text(rect.get_x() + rect.get_width()/2.0, height - 20, 'fn = ' + str(round(cm_values[3][indexing])), ha='center', va='bottom')
        indexing+=1