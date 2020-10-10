"""
Module for interactive exploration of matplotlib scatter plots
"""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


def _get_closest(click_point,data):
    """
    
    Get index of a point in data, that has the smallest Eucledian distance to click_point
    
    Parameters:
    -----------
    click_point: tuple of floats
           x and y of a particular point, in units of data
    data : 2d numpy array of list of arrays with shape (Nx2),
           where N-number of data points, that contains coordinates.
           
    Returns:
    --------
    best_point : int
                Index of the point in data, that is the closest to click_point
    best_distance : Distance to that point
    """
    # To do: add point removal on repeating click
    data_array = np.array(data).T
    point_array = np.array(click_point).reshape(2,1)
    square_distance_array = np.sum(np.square(np.subtract(data_array,point_array)),axis=0)    
    best_point_ndx = np.argmin(square_distance_array)
    best_distance = np.sqrt(square_distance_array[best_point_ndx])
    return best_point_ndx, best_distance


def label_point(fig, ax, scatter_object,labels,highlight_color='red',remove_on_click=True):
    """
    Provides infrastructure for interactive labeling of scatter plots.
    
    parameters:
    fig : matplotlib.figure.Figure
    ax : matplotlib.axes._subplots.AxesSubplot object
    scatter_object : matplotlib.collections.PathCollection
    highlight_color : str
                    Name of color used to highlight a point
    remove_on_click : bool (default True)
                    If true, repeated click near the highlighted point removes a label and change color of the point
                    to the original one.
    """
    # obtain plotted data
    data = scatter_object.get_offsets()
    label_color_rgb = colors.to_rgba(highlight_color)
    n_points = len(data) # number of points in dataset
    # Get current colors. Check, if colors are represented as a single color or an array of colors
    initial_colors = scatter_object.get_facecolor()
    if len(initial_colors) == 1: # If single color, convert into array
        initial_colors = np.array([initial_colors[0,:] for i in range(n_points)])
    else:
        initial_colors = custom_colors
    label=ax.annotate('',data[0])
    
    def onclick(event):
        # event.button, event.x, event.y, event.xdata, event.ydata : usefull atributes of an event
        data = scatter_object.get_offsets()
        best_point, best_distance = _get_closest((event.xdata,event.ydata),data)
        new_colors = initial_colors.__copy__()
       
        current_colors = scatter_object.get_facecolor() # look at current colors
        if len(current_colors) == 1:
            current_colors = np.array([current_colors[0,:]for i in range(n_points)])
            
        best_point_color = current_colors[best_point]  # current color of the chosen point
        
        # If best point is already highlighted, remove highlight and label
        if (remove_on_click and np.all(best_point_color == label_color_rgb)):
            label.set_text("")
            new_colors[best_point] = initial_colors[best_point]
            scatter_object.set_facecolors(new_colors)
        # If current point is not highlighted, highlight it and place a new label
        else: 
            new_colors[best_point] = label_color_rgb
            scatter_object.set_facecolors(new_colors)
            label.set_text("{}".format(labels[best_point]))
            label.set_x(event.xdata)
            label.set_y(event.ydata)
    cid = fig.canvas.mpl_connect('button_press_event', onclick);