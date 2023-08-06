# -*- coding: utf-8 -*-
"""
Generates random data to be used for demoing purposes.
Created on Tue May 14 13:53:18 2019

@author: ecramer 
"""

import numpy as np
import pandas as pd

def genClusterData(n_obs, n_clusters):
    """
    Generates cluster data.
    """
    # calculate the probability of belonging to each cluster
    cluster_probs = [np.random.randint(1, 100, 1)[0] for i in range(n_clusters)]
    cluster_probs = [i/sum(cluster_probs) for i in cluster_probs]
    # generate the clusters given their probabilities
    clusters = np.random.choice(n_clusters, size=n_obs, replace=True, p=cluster_probs)
    return clusters, cluster_probs

def genStageData(n_obs, n_stages, n_clusters, cluster_data):
    # make a grid of probabilities 
    # clusters are columns
    # stages are rows
    # each column sums to one
    # columns are the probabilities of an observation in that cluster belonging to each stage
    # probabilities follow a linear mapping
    
    p_mat = np.zeros((n_stages, n_clusters))
    p_mat[0, :] = (np.linspace(1, 100, n_clusters)/np.linspace(1, 100, n_clusters).sum())[::-1]
    for i in range(1, n_stages):
        p_mat[i, :] = np.roll(p_mat[i-1, :], 1)
    for i in range(n_clusters):
        adj = (1 - p_mat[:, i].sum())/n_stages
        p_mat[:, i] = p_mat[:, i] + adj
    
    # for each observation
    stages = np.zeros((n_obs))
    for i in range(n_obs):
        ob = cluster_data[i]
        stages[i] = np.random.choice(n_stages, p = p_mat[:, ob])
    return stages, p_mat

def formData(data):
    """
    Re-format the dataframe into an adjusted pivot table. Assumes columns are named 'cluster' and 'satge'.
    
    Input:
        data (pandas dataframe): the dataframe to pivot and adjust
    
    Output:
        returns a pivot table of the data that has been adjusted to give percentages
    """
    pivoted = data.pivot_table(columns='stage', index=['cluster'], aggfunc={'stage':'count'})
    pivoted.reset_index(inplace=True)
    pivoted['sum'] = pivoted.drop('cluster', axis=1).sum(axis=1)
    pivoted2 = pivoted.loc[:, 'stage'].div(pivoted['sum'], axis=0)
    return pivoted2

def generateData(n_obs = 1000, n_stages = 5, n_clusters = 12):
    """
    Generates random data for demoing.
    
    Input:
        n_obs (int): the number of observations
        n_stages (int): the number of stages
        n_clusters (int): thenumber of clusters
    
    Output:
        a list with the clusters and stages randomly generated
    """
    # generate the stage and cluster data
    cluster_data, _ = genClusterData(n_obs, n_clusters)
    stage_data, _ = genStageData(n_obs, n_stages, n_clusters, cluster_data)
    stage_data = np.random.randint(0, high = n_stages, size = n_obs)
    cluster_data = np.random.randint(0, high = n_clusters, size = n_obs)
    # put the stage and cluster data into a dataframe, then pivot and set the sum of all rows=1
    data = pd.DataFrame({'cluster':cluster_data, 'stage':stage_data})
    return formData(data)

def _test():
    generateData()

if __name__ == "__main__":
    _test()