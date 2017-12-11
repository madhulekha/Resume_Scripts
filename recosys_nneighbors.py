# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 13:01:09 2016

@author: madhu
"""
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv
from math import sqrt
from itertools import combinations
from copy import deepcopy
from matplotlib.colors import ListedColormap
from sklearn import neighbors
import numpy as np

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    # Find the number of elements
    n=len(si)
    # if they are no ratings in common, return 0
    if n==0: return 0
    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r
    
# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(prefs,person,other)
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings

# A dictionary of patients and their ratings of a small
# set of doctors
critics={'Madhu': {'Isabella': 2.5, 'Aiden': 3.5,
'Sofia': 3.0, 'Samantha': 3.5, 'Hudson': 2.5,
'Eleanor': 3.0},
'Teja': {'Isabella': 3.0, 'Aiden': 3.5,
'Sofia': 1.5, 'Samantha': 5.0, 'Eleanor': 3.0,
'Hudson': 3.5},
'Aditya': {'Isabella': 2.5, 'Aiden': 3.0,
'Samantha': 3.5, 'Eleanor': 4.0},
'Ahmed': {'Aiden': 3.5, 'Sofia': 3.0,
'Eleanor': 4.5, 'Samantha': 4.0,
'Hudson': 2.5},
'Don': {'Isabella': 3.0, 'Aiden': 4.0,
'Sofia': 2.0, 'Samantha': 3.0, 'Eleanor': 3.0,
'Hudson': 2.0},
'Jack': {'Isabella': 3.0, 'Aiden': 4.0,
'Eleanor': 3.0, 'Samantha': 5.0, 'Hudson': 3.5},
'Toby': {'Aiden':4.5,'Hudson':1.0,'Samantha':4.0}}

critics_df = DataFrame(critics)
#Saving this as a csv to show
critics_df.to_csv('initial_reco_show.csv')

#Doing the following steps to show an example plot
labels = critics_df.index

#Doing the following to show an example plot
fig = plt.figure()
ax = fig.add_subplot(111)

#plt.subplots_adjust(bottom = 0.1)
ax.scatter(critics_df['Don'], critics_df['Teja'])
plt.xlabel('Don')
plt.ylabel('Teja')
plt.xlim(critics_df['Don'].min()-1, critics_df['Don'].max()+1)
plt.ylim(critics_df['Teja'].min()-1, critics_df['Teja'].max()+1)

for i, txt in enumerate(labels):
    ax.annotate(txt, (critics_df['Don'][i],critics_df['Teja'][i]))
    
plt.savefig('sample_correlation_1.png')
plt.close()

#Doing the following to show an example plot
fig = plt.figure()
ax = fig.add_subplot(111)

#plt.subplots_adjust(bottom = 0.1)
ax.scatter(critics_df['Aditya'], critics_df['Madhu'])
plt.xlabel('Aditya')
plt.ylabel('Madhu')
plt.xlim(critics_df['Aditya'].min()-1, critics_df['Aditya'].max()+1)
plt.ylim(critics_df['Madhu'].min()-1, critics_df['Madhu'].max()+1)

for i, txt in enumerate(labels):
    ax.annotate(txt, (critics_df['Aditya'][i],critics_df['Madhu'][i]))
    
plt.savefig('sample_correlation_2.png')
plt.close()

#Creating a list of similarities between people
temp_dict = [{'Person1':i[0], 'Person2':i[1], 'Corr':sim_pearson(critics, i[0],i[1])}\
             for i in combinations(critics.keys(),2)]
DataFrame(temp_dict).to_csv('corr_show.csv', index = False)

final = deepcopy(critics_df)
#Getting out the recommendations
for person in critics_df.columns:
    recos = getRecommendations(critics, person)
    if recos:
        for i in recos:
            final.loc[i[1],person] = i[0]
            
final.to_csv('final_reco_show.csv')

########################################################################################
##Nearest Neighbors starts here
n_neighbors = 15

dat = read_csv('input_classification.csv')

# import some data to play with
X = np.array(dat[['feature1','feature2']])  # we only take the first two features. We could
                      # avoid this ugly slicing by using a two-dim dataset
y = np.array(dat['label'])

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))
    plt.xlabel('feature1')
    plt.ylabel('feature2')
              
    plt.savefig('out_'+weights+'.png')
    plt.close()