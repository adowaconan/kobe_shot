#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:37:21 2018

@author: nmei
"""
from matplotlib import pyplot as plt
#from http://savvastjortjoglou.com/nba-shot-sharts.html
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib as mpl
import pandas as pd
import numpy as np

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-45, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                          fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                          fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                     color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                    color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def preprocess(df_name = '../data/kobe.csv'):
    df = pd.read_csv(df_name)
    df.set_index('shot_id',inplace=True)
    column_object = ['action_type']
    column_category = ['combined_shot_type',
                       'game_event_id',
                       'game_id',
#                       'period',
                       'playoffs',
                       'season',
                       'shot_made_flag',
                       'shot_type',
                       'team_id']
    for column in column_object:
        df[column] = df[column].astype('object')
    for column in column_category:
        df[column] = df[column].astype('category')
    
    # data cleaning
    df['game_data_DT'] = pd.to_datetime(df['game_date'])
    df['dayofweek'] = df['game_data_DT'].dt.dayofweek
    df['dayofyear'] = df['game_data_DT'].dt.dayofyear
    df['secondsFromPeriodEnd'] = 60*df['minutes_remaining']+df['seconds_remaining']
    df['secondsFromPeriodStart'] = 60*(12-df['minutes_remaining'])+(60-df['seconds_remaining'])
    df['secondsFromGameStart'] = (df['period']<=4).astype(int)*(df['period']-1)*12*60+ (df['period']>4).astype(int)*((df['period']-4)*5*50+4*12*60) + df['secondsFromPeriodStart']
    
    # transformation
    df['seconds_from_period_end'] = 60 * df['minutes_remaining'] + df['seconds_remaining']
    df['last_5_sec_in_period'] = df['seconds_from_period_end'] < 5
    
    
    # Matchup - (away/home)
    df['home_play'] = df['matchup'].str.contains('vs').astype('int')
    df.drop('matchup',axis = 1,inplace = True)
    
    ## Loc_x, Loc_y binning
    #df['loc_x'] = pd.cut(df['loc_x'],25)
    #df['loc_y'] = pd.cut(df['loc_y'],25)
    
    # replace 20 least common action types with value 'other'
    rare_action_types = df['action_type'].value_counts().sort_values().index.values[:20]
    df.loc[df['action_type'].isin(rare_action_types), 'action_type'] = 'other'
    return df

def Draw2DGaussians(gaussianMixtureModel,ellipseColors,ellipseTextMessages,ax):
    for ii, (mean,covarianceMatrix) in enumerate(zip(gaussianMixtureModel.means_,
                                                     gaussianMixtureModel.covariances_)):
        v,w = np.linalg.eigh(covarianceMatrix)
        v = 2.5 * np.sqrt(v) # go to units of standard deviation instead of variance
        
        # calculate the ellipse angle and 2 axis length and draw it
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan(u[1]/u[0])
        angle = 180 * angle / np.pi # convert to degrees
        currEllipse = mpl.patches.Ellipse(mean,
                                          v[0],
                                          v[1],
                                          180 + angle,
                                          color = ellipseColors[ii])
        currEllipse.set_alpha(0.5)
        ax.add_artist(currEllipse)
        ax.text(mean[0]+7,
                mean[1]-1,
                ellipseTextMessages[ii],
                fontsize = 13,
                color = 'blue',)











































