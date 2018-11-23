# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 16:52:17 2018

@author: ning

Copy and paste from kaggle.com/selfishgene/psychology-of-a-professional-althlete

"""

import os
import pandas as pd
import numpy as np
import utils
from matplotlib import pyplot as plt
from sklearn import mixture
import seaborn as sns
sns.set_style('white')
sns.set_context('poster')

figure_dir = '../figures'
if not os.path.exists(figure_dir):
    os.mkdir(figure_dir)

df = utils.preprocess('../data/kobe.csv')

numGaussians = 12
gaussianMixtureModel = mixture.GaussianMixture(n_components = numGaussians,
                                               covariance_type = 'full',
                                               init_params = 'kmeans',
                                               n_init = 50,
                                               verbose = 0,
                                               random_state = 12345)
gaussianMixtureModel.fit(df[['loc_x','loc_y']].values)
# add the GMM cluster as a field in the data
df['shotLocationCluster'] = gaussianMixtureModel.predict(df[['loc_x','loc_y']].values)

fig,ax = plt.subplots(figsize=(15,15))
ellipseTextMessages = ['{:.2f} %'.format(100*gaussianMixtureModel.weights_[x]) for x in range(numGaussians)]
ellipseColors = ['red',
                 'green',
                 'purple',
                 'cyan',
                 'magenta',
                 'yellow',
                 'blue',
                 'orange',
                 'silver',
                 'maroon',
                 'lime',
                 'olive',
                 'brown',
                 'darkblue',]
utils.Draw2DGaussians(gaussianMixtureModel,ellipseColors,ellipseTextMessages,ax)
ax = utils.draw_court(ax=ax,outer_lines=True)
ax.set(xlim=(-250,250),
       ylim=(-48,423),
       xlabel='',
       ylabel='',
       title='shot attempts')
plt.axis('off')
fig.savefig(os.path.join(figure_dir,'shot attempts cluster.png'),
            dpi = 300, bbox_inches = 'tight')

# make sure the gaussian model actually capture something, so that it makes 
# sense to assign the shots accordingly
fig,ax = plt.subplots(figsize=(15,15))
ax.scatter(x = df['loc_x'].values,
           y = df['loc_y'].values,
           c = df['shotLocationCluster'].values,
           s = 40, 
           cmap = 'hsv',
           alpha = 0.1,)
ax = utils.draw_court(ax=ax,outer_lines=True)
ax.set(xlim=(-250,250),
       ylim=(-48,423),
       xlabel='',
       ylabel='',
       title='shot attempts')
plt.axis('off')
fig.savefig(os.path.join(figure_dir,'shot attempts assigned clusters.png'),
            dpi = 300, bbox_inches = 'tight')

# shot accuracy
clusterAccuracy = {}
for area in pd.unique(df['shotLocationCluster']):
    shotsAttempted = np.sum(df['shotLocationCluster'] == area)
    shotsMade = np.sum(np.logical_and(df['shotLocationCluster']==area,
                                      df['shot_made_flag']==1))
    clusterAccuracy[area] = float(shotsMade) / shotsAttempted

ellipseTextMessages = ['{:.2f} %'.format(100*clusterAccuracy[x]) for x in range(numGaussians)]
fig,ax = plt.subplots(figsize=(15,15))
ellipseTextMessages = ['{:.2f} %'.format(100*gaussianMixtureModel.weights_[x]) for x in range(numGaussians)]
ellipseColors = ['red',
                 'green',
                 'purple',
                 'cyan',
                 'magenta',
                 'yellow',
                 'blue',
                 'orange',
                 'silver',
                 'maroon',
                 'lime',
                 'olive',
                 'brown',
                 'darkblue',]
utils.Draw2DGaussians(gaussianMixtureModel,ellipseColors,ellipseTextMessages,ax)
ax = utils.draw_court(ax=ax,outer_lines=True)
ax.set(xlim=(-250,250),
       ylim=(-48,423),
       xlabel='',
       ylabel='',
       title='shot accuracy')
plt.axis('off')
fig.savefig(os.path.join(figure_dir,'shot accuracy by areas.png'),
            dpi = 300,bbox_inches='tight')









