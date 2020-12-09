# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 04:35:31 2020

@author: Ege
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

def plot_active_hours(df, color='#ffdfba', savefig=False, dpi=100, user='All'):
    """ Plot active hours of a single user or all 
    users in the group. A bar is shown if in that hour
    user(s) are active by the following standard:
    
    If there are at least 20% of the maximum hour of messages
    
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe of all messages
    color : str, default '#ffdfba'
        Hex color of bars
    savefig : boolean, deafult False
        Whether or not to save the figure instead of showing
    dpi : int, default 100
        Resolution of the figure you want to save
    user : str, default 'All'
        Variable to choose if you want to see the active hours
        of a single user or all of them together. 'All' shows 
        all users and the name of the user shows that user. 
    
    """
    # Prepare data for plotting
    if user != 'All':
        df = df.loc[df.User == user]
        title = 'Active hours of {}'.format(user)
    else:
        title = 'Active hours of all users'
    df['Hour'] = df['Date'].dt.hour
    hours = df.Hour.value_counts().sort_index().index
    count = df.Hour.value_counts().sort_index().values
    font = {'fontname':'Comic Sans MS'}

    # Only get active hours
    count = [1 if x > (.2 * max(count)) else 0 for x in count]

    # Plot figure
    fig, ax = plt.subplots()
    
    # Then plot the right part which covers up the right part of the picture
    ax.bar(hours, count, color=color,align='center', width=1,
            alpha=1, lw=4, edgecolor='w', zorder=2)

    # Set ticks and labels
    ax.yaxis.set_ticks_position('none') 
    ax.set_yticks([])
    ax.set_ylabel('', labelpad=50, rotation='horizontal',
                   color="#6CA870",**font)
    ax.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 24])
    ax.set_xticklabels(["Midnight", "3 AM", "6 AM", "9 AM", "Noon", "3 PM", "6 PM", "9 PM", 
                       "Midnight"], **font)
    plt.title(title, y=0.8)
    
    # Create horizontal line instead of x axis
    plt.axhline(0, color='black', xmax=1, lw=2, zorder=3, clip_on=False)

    # Make axes white to remove any image line that may be left
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')

    # Remove the left and bottom axis
    ax.spines['left'].set_visible(False)

    # Set sizes
    fig.set_size_inches((13.5, 1))
    fig.tight_layout(rect=[0, 0, .8, 1])

    # Save or show figure    
    if savefig:
        plt.savefig(f'results/{savefig}active_hours.png', dpi = dpi)
    else:
        plt.show()

def plot_messages(df, colors=None, trendline=False, savefig=False, dpi=100):
    """ Plot the weekly count of messages per user
    
    Parameters:
    -----------
    df : pandas dataframe
        Dataframe containing all messages
    colors : list, default None
        List of colors to be used for the plot. 
        Matplotlib colors are chosen if None. 
    trendline : boolean, default False
        Whether are not there will be a trendline for the 
        combined count of messages
    savefig : boolean, default False
        Whether or not to save the figure instead of showing
    dpi : int, default 100
        Resolution of the figure you want to save
    
    """
        
    # Prepare data
    if not colors:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color'] * 10

    df = df.set_index('Date')   
    users = {user: df[df.User == user] for user in df.User.unique()}
    
    # Resample to a week by summing
    for user in users:
        users[user] = users[user].resample('7D').count().reset_index()
    
    # Create figure and plot lines
    fig, ax = plt.subplots()
    legend_elements = []
    
    for i, user in enumerate(users):
        ax.plot(users[user].Date, users[user].Body, linewidth=3, color=colors[i])
        legend_elements.append(Line2D([0], [0], color=colors[i], lw=4, label=user))

    # calc the trendline
    if trendline:
        x = [x for x in users[user].Date.index]
        y = users[user].Body.values
        z = np.polyfit(x, y, 5)
        p = np.poly1d(z)
        ax.plot(users[user].Date, p(x), linewidth=2, color = 'g')

    # Remove axis
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    font = {'fontname':'Comic Sans MS', 'fontsize':14}
    ax.set_ylabel('Nr of Messages', {'fontname':'Comic Sans MS', 'fontsize':14})
    ax.legend(handles=legend_elements, bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.)

    # Set size of graph
    fig.set_size_inches(20, 10)
    
    # Creating custom legend
    custom_lines = [Line2D([], [], color=colors[i], lw=4, 
                          markersize=6) for i in range(len(colors))]

    # Create horizontal grid
    ax.grid(True, axis='y')
    
    # Legend and title
    ax.legend(custom_lines, [user for user in users.keys()], bbox_to_anchor=(1.05, 1), loc=2,
              borderaxespad=0.)
    plt.title("Weekly number of messages per user", fontsize=20)
    
    if savefig:
        plt.savefig(f'results/moments.png', format="PNG", dpi=dpi)
    else:
        plt.show()
        

