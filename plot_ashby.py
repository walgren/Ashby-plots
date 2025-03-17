'''
This script will plot various material properties in an 'Ashby-type' way (
i.e., convex hulls surrounding points of certain classes). 

Input file format: one excel file, with either material property ranges or 
single values defined. 

Dependencies:
    files: plot_convex_hull.py
           rotation_aware_annotation.py
           plot_utilities.py
           math_utilities.py
    python modules:
        os (pre-installed)
        pandas
        numpy
        matplotlib
        scipy
        sklearn

'''
import os

import pandas as pd

import matplotlib.pyplot as plt

from src.plot_utilities import (
    create_legend,
    draw_plot,
    plotting_presets,
    draw_guideline, 
    common_definitions,
    )


if __name__ == '__main__':
    #%% USER INPUTS (everything you will need to change *should* be here)
    # FIXME To-do:
    '''
        # Error handling/format checking for:
        #   file type
        # Create inputs for:
            # guideline power (figure out what to call that)
            # guideline x_limits and y_intercept
            # guideline string
    '''


    # file with all of your material data (must be xlsx)
    
    file_name = 'common_material_properties.xlsx'

    data_type = 'ranges' # type of material data ('ranges' or single 'values')

    figure_type = 'presentation' #options are 'publication' or 'presentation'
    figure_size = (9,7) #width, height, in inches

    # quantities you would like to plot
    x_axis_quantity = 'Density'
    # x_axis_quantity = 'Density'
    # y_axis_quantity = "Young Modulus"
    y_axis_quantity = "Poisson difference"

    # x- and y-axes limits
    # x_lim = [1E-4,1E3]
    x_lim = [10, 30000] #min, max
    y_lim = [0.5,1.1] #min, max
    # y_lim = [1E-4,1E3]

    #Flag to plot in log-log space
    log_flag = True

    # Guideline setup
    guideline_flag = True

    if guideline_flag == True:
        guideline = {
            'power':1, #power to plot the guideline on (e.g., 1/3, 1)
            'x_lim':[1E1, 1E5], #x-limits of the guideline (not necessarily the figure x limits)
            # 'string':r"$\frac{E^{1/3}}{\rho} \equiv k$", #string to display
            'string':r"$\frac{1}{(1+\nu)\rho} \equiv k$",
            'y_intercept': 0.001, #y-intercept of the guideline, 0.001 for poisson, 1E-10 for stiffness
            'string_position': (300,0.51) , #location of the annotation, (300,0.51) for poisson, (65, 2E-4) for stiffness
            }
        
    # Flag to plot individual materials as stars. 
    individual_material_flag = False
    if individual_material_flag == True: 
        foam = {
            'E':0.124E-3,
            'nu':0.45,
            'rho':400,
            }
        
        PLA = {
            'E':2.009,
            'nu':0.3,
            'rho':1300,
            }
        
        marker_size = 500
    


    #%% General setup
    # Create dictionaries with common units bases etc.
    units, material_colors = common_definitions()

    # Set up baseline plot formatting
    plotting_presets(figure_type)

    #load data
    file_path = os.path.join(
        os.getcwd(),
        'material_properties',
        file_name,
        )
    
    data = pd.read_excel(
        file_path
        )

    # Error handling about the colors dictionary
    if set(data.groupby('Category').groups) > set(material_colors):
        raise ValueError('You have material categories that have not been assigned \
a color. Please add a color to the material_colors dictionary (common_definitions function).')

    #%% Figure manipulation

    #Create figure
    fig, ax = plt.subplots(1,1, figsize=figure_size)

    # set x- and y-labels
    try:
        if y_axis_quantity == 'Poisson difference':
            y_label = r'Hyperbolic Poisson Ratio $\frac{1}{1+\nu}$, '+ units[y_axis_quantity]
        else:
            y_label = y_axis_quantity + ', ' + units[y_axis_quantity]
            
        if x_axis_quantity == 'Poisson difference':
            x_label = r'Hyperbolic Poisson Ratio $\frac{1}{1+\nu}$, '+ units[x_axis_quantity]
        else:
            x_label = x_axis_quantity + ', ' + units[x_axis_quantity]


        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    except:
        raise ValueError("Could not set correct x- and y-labels. \
Make sure your x_axis_quantity and y_axis_quantity \
have equivalent key-value pairs in the units dictionary (common_definitions function).")

    #set axes limits
    ax.set(xlim=x_lim, ylim= y_lim)

    #toggle log-log plot
    if log_flag == True:
        ax.loglog()

    # set x-scale to logarithmic
    # ax.set_xscale('log')

    #add grid lines
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.htmls
    ax.grid(
        which = 'major',
        axis = 'both',
        linestyle = '-.',
        zorder = 0.5)

    #%% Data plotting
    if guideline_flag == True:
        #draw guideline
        draw_guideline(
                guideline,
                ax = ax,
                log_flag = log_flag,
                )

    if (x_axis_quantity == 'Poisson difference') or (y_axis_quantity == 'Poisson difference'):

        data['Poisson difference high'] = 1/(1+data['Poisson low'])
        data['Poisson difference low'] = 1/(1+data['Poisson high'])

    draw_plot(
            data,
            x_axis_quantity,
            y_axis_quantity,
            ax,
            material_colors,
            data_type = data_type,
            )

    create_legend(
            material_classes = data.groupby('Category').groups.keys(),
            material_colors = material_colors,
            )
      
    # plot discrete materials
    if individual_material_flag == True:
        ax.scatter(
            foam['rho'],
            # foam['E'],
            1/(1+foam['nu']),
            c = 'b',
            edgecolors ='k',
            marker = '*',
            s = marker_size,
            )
        
        ax.scatter(
            PLA['rho'],
            # PLA['E'],
            1/(1+PLA['nu']),
            c = 'r',
            edgecolors ='k',
            marker = '*',
            s = marker_size,
            )
