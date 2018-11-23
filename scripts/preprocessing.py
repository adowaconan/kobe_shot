#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:14:20 2018

@author: nmei
"""

import pandas as pd
import utils
from matplotlib import pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_context('poster')

data = pd.read_csv('kobe.csv')
data.set_index('shot_id',inplace=True)
column_object = ['action_type']
column_category = ['combined_shot_type',
                   'game_event_id',
                   'game_id',
                   'period',
                   'playoffs',
                   'season',
                   'shot_made_flag',
                   'shot_type',
                   'team_id']
for column in column_object:
    data[column] = data[column].astype('object')
for column in column_category:
    data[column] = data[column].astype('category')

# data cleaning
df = data.copy()
column_drop = ['team_id',
               'lat',
               'lon',
               'game_id',
               'game_event_id',
               'team_name',
#               'shot_made_flag',
               ]
for column in column_drop:
    df.drop(column,axis = 1,inplace = True)

# transformation
df['seconds_from_period_end'] = 60 * df['minutes_remaining'] + df['seconds_remaining']
df['last_5_sec_in_period'] = df['seconds_from_period_end'] < 5
column_drop = ['minutes_remaining',
               'seconds_remaining',
               'seconds_from_period_end']
for column in column_drop:
    df.drop(column,axis = 1,inplace = True)

# Matchup - (away/home)
df['home_play'] = df['matchup'].str.contains('vs').astype('int')
df.drop('matchup',axis = 1,inplace = True)

## Loc_x, Loc_y binning
#df['loc_x'] = pd.cut(df['loc_x'],25)
#df['loc_y'] = pd.cut(df['loc_y'],25)

# replace 20 least common action types with value 'other'
rare_action_types = df['action_type'].value_counts().sort_values().index.values[:20]
df.loc[df['action_type'].isin(rare_action_types), 'action_type'] = 'other'

fig,ax = plt.subplots(figsize=(15,15))
colors = ['grey','red']
for made,color in zip(pd.unique(df.dropna().shot_made_flag),colors):
    ax.scatter(df[df['shot_made_flag'] == made]['loc_x'],
               df[df['shot_made_flag'] == made]['loc_y'],
               c=color,
#               s = 2,
               alpha=0.5)
ax = utils.draw_court(ax=ax,outer_lines=True)
ax.set(xlim=(-250,250),
       ylim=(-48,423),
       xlabel='',
       ylabel='',)