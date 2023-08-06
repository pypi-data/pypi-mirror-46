# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:52:16 2019

@author: ecramer <eric.cramer@curie.fr>
"""
# imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import collections, tqdm
from utils import calcCentroid, cartToPolar, adjustColor
from generate import formData

## Plotting the center of mass on a polar graph
# treat each row of the pop_counts_p as radii, and each timepoint equally spaced as an angle measure

def calcPolarCentroids(data):
    """
    Calculates polar centroids for each cluster/population.
    
    Input:
        data (2D numpy array): the data to calculate polar centroids for. Each row is a population/cluster 
        and each column is a stage's percentage component of that cluster.
    
    Output:
        2D array of centroid positions in r, theta format
    """
    centroids = []
    for i in tqdm.tqdm(range(data.shape[0])):
        radii = [data[s].values[i] for s in data.columns]
        angles = np.deg2rad(np.arange(0, 360, 360/data.shape[1]))
        centroids.append(calcCentroid(radii, angles))
    # create a list with the centroids as polar coordinates
    centroids_polar = np.asarray([cartToPolar(a[0], a[1]) for a in centroids])
    return centroids_polar

def calcClusterSizes(cluster_data):
    """
    Calculates the size of clusters for plotting.
    
    Input:
        cluster_data (1D list): a list of the observations and which cluster they belong to.
    
    Output:
        returns the sizes of the clusters in a logarithmic scale
    """
    # point sizes
    cluster_freqs = collections.Counter(cluster_data)
    cluster_sizes = sorted([(key, cluster_freqs[key]) for key in cluster_freqs.keys()], key=lambda x: x[0])
    cluster_sizes = np.asarray([a[1] for a in cluster_sizes])
    cluster_sizes = 2**abs(np.log(10000*cluster_sizes/cluster_sizes.max()))
    return cluster_sizes
    
# point colors
def genColors(data):
    """
    Generates colors for plotting.
    
    Input: 
        n_clusters (int): the number of clusters 
    
    Output:
        returns a list of matplotlib compatible colors for plotting
    """
    cmap = plt.get_cmap('brg')
    colors = cmap(range(data.shape[0]))
    colors = [adjustColor(c[:-1], 2) for c in colors]
    return colors

def plotUtility(centroids_polar, cluster_sizes, colors, stage_labels, theta_max=360):
    """
    Plots the clockplot
    
    Input:
        centroids_polar:  2D array of centroid positions in r, theta format
        cluster_sizes: the sizes of the clusters in a logarithmic scale
        colors: the color for each cluster when plotting
        stage_labels: the label to put on the axes for each stage
        theta_max: the maximum angle (or x value in cartesian format)
        
    Output:
    
    """
    # set up the plot aesthetics
    # point positions
    theta = [a[1] for a in centroids_polar]
    r = [a[0] for a in centroids_polar]
    
    # set up the figure
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='polar')
    sc = [None]*len(theta)
    # iteratively plot each of the points
    for i in tqdm.tqdm(range(len(theta))):
        sc[i] = ax.scatter(theta[i], 3*r[i], cmap=colors[i], label=i+1, alpha=(100-i)/100, s=cluster_sizes[i], edgecolor='black')
    
    # setting the x axis range
    ax.set_thetamin(0)
    ax.set_thetamax(theta_max)
    
    # setting the order for the x axis
    ax.set_theta_zero_location("N")  # theta=0 at the top, like a clock
    ax.set_theta_direction(-1) 
    
    # set the x labels
    ax.set_xticks(np.deg2rad(np.arange(0, theta_max, theta_max/len(stage_labels))))
    ax.set_xticklabels(stage_labels, fontweight='bold')
    
    ax.set_rlabel_position(-45)
    
    plt.title('Cluster Center of Mass')    
    plt.legend(sc, np.arange(1, 65), title='Cluster', ncol=8, loc='center', bbox_to_anchor=(0.5, -0.2))
    
    # Show polar plot
    plt.show()
    
    # return the figure
    return fig

def plotClockplot(data, cluster_data, stage_labels, theta_max=360):
    """
    Everything, from data to graph.
    
    Input:
        data (2D numpy array or pandas dataframe): the data in pivot table format with columns as stages and clusters as rows 
        cluster_data (1D list or array):  the clusters of the observations
        stage_labels (1D list of strings): the labels for the different stages to plot 
        theta_max (int): indicates the largest theta/X in degrees
    
    Output:
        returns the clockplot figure
        
    """    
    centroids_polar = calcPolarCentroids(data)
    cluster_sizes = calcClusterSizes(cluster_data)
    cluster_colors = genColors(data)
    return plotUtility(centroids_polar, cluster_sizes, cluster_colors, stage_labels, theta_max)

def _demo():
    print("Demoing the clockplot.")
    lineardemo = pd.read_csv('../data/lineardemo.csv')
    pivoted = formData(lineardemo)
    plotClockplot(pivoted, lineardemo['cluster'].values, list(set(lineardemo.stage.values)), theta_max=360)

if __name__ == "__main__":
    _demo()