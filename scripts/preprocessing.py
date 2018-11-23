#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:14:20 2018

@author: nmei
"""

import os
import pandas as pd
import numpy as np
import utils
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_context('poster')

figure_dir = '../figures'
if not os.path.exists(figure_dir):
    os.mkdir(figure_dir)

df = utils.preprocess('../data/kobe.csv')

fig,ax = plt.subplots(figsize=(15,15))
colors = ['grey','red']
labels = ['missed','made']
for made,color,label in zip(pd.unique(df.dropna().shot_made_flag),colors,labels):
    ax.scatter(df[df['shot_made_flag'] == made]['loc_x'],
               df[df['shot_made_flag'] == made]['loc_y'],
               c=color,
#               s = 2,
               alpha=0.5,
               label=label)
ax = utils.draw_court(ax=ax,outer_lines=True)
ax.legend(loc='best')
ax.set(xlim=(-250,250),
       ylim=(-48,423),
       xlabel='',
       ylabel='',)
plt.axis('off')
fig.savefig(os.path.join(figure_dir,'shot mades.png'),
            dpi = 300, bbox_inches = 'tight')