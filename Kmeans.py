##AUTHOR: ROMAN BELAIRE
##NOVEMBER 10TH, 2019
#
#This program contains my implementation of the ID3 decision tree algorithm.
#
##################
import pandas as pd
import math
import argparse
import random
from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np

def distance_between(p1, p2):
    total = 0
    for i in range(len(p1)):
        total += (p1[i] - p2[i])**2
    return math.sqrt(total)

def k_means(input_set, k):
    #find random k centroids
    centroids = []
    rand_center_indicies = random.sample(range(0, len(input_set)), k)
    print(rand_center_indicies)
    for index in rand_center_indicies:
        centroids.append(input_set[index])


    while True:
        centroid_groups = []
        for i in range(0,k):
            a = []
            for j in range(0,len(input_set[0])):
                a.append(0)
            centroid_groups.append(a)
        centroid_group_size = [0] * k
        
        for point in input_set:
            closest_centroid = 0
            closest_distance = -1
            for i in range(0,k):
                distance = distance_between(centroids[i], point)
                if closest_distance == -1 or distance < closest_distance:
                    closest_distance = distance
                    closest_centroid = i
            #print("%s closest_centroid: %s, distance %s" % (point, centroids[closest_centroid], closest_distance))
            for dimension in range(len(point)):
                #print("adding %s to centroid %s: %s, dimension %s" % (point[dimension], closest_centroid, centroid_groups[closest_centroid], dimension))
                centroid_groups[closest_centroid][dimension] += point[dimension]
            centroid_group_size[closest_centroid] += 1

        #print(centroid_groups)
        #get new centroids
        for i in range(len(centroid_groups)):
            for j in range(len(centroid_groups[i])):
                centroid_groups[i][j] = centroid_groups[i][j] / centroid_group_size[i]
        #check if they changed
        if centroid_groups == centroids:
            break
        else:
            centroids = centroid_groups
            print(centroids)

    #make final groups and plot
    fig = plt.figure()
    plot = fig.add_subplot(1,1,1)

    final_groups = []
    for i in range(k):
        final_groups.append([])

    for point in input_set:
        closest_centroid = 0
        closest_distance = -1
        for i in range(0,k):
            distance = distance_between(centroids[i], point)
            if closest_distance == -1 or distance < closest_distance:
                closest_distance = distance
                closest_centroid = i
        final_groups[closest_centroid].append(point)

    colors = ('red','blue','green')#plt.cm.get_cmap('hsv', k)
    params = [0] * len(input_set[0])
    for color, data in zip(colors, final_groups):
        x = [row[0] for row in data]
        y = [row[1] for row in data]
        plot.scatter(x, y, c=color)
    centroids_x = [row[0] for row in centroids]
    centroids_y = [row[1] for row in centroids]
    plot.scatter(centroids_x, centroids_y, c='black')
    plt.title('Final Groupings')
    plt.show()
    return centroids


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path")
    argparser.add_argument("k")
    args = argparser.parse_args()
    data = pd.read_csv('k_means_data.csv').values.tolist()
    k = int(args.k)

    print(sorted(k_means(data, k)))
