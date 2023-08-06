# -*- Mode: python
#
# Licenses 
# Authors

"""\
Functions to handle openDX files
================================

Comments

Functions
----------------

.. dict2grd
.. grd4smooth
.. grd2dx
.. dx4resample

"""

###########################################################################
#### imports								  #
###########################################################################

import numpy as np

from gridData import Grid, OpenDX
from scipy.ndimage.filters import gaussian_filter

###########################################################################
#### functions / classses                                                 #
###########################################################################

def dict2grd(data):
        """Comments"""

        # get value of dict
        order = [i[1].ods
                        for i in data.items()]
        # get keys of dict
        rf = lambda x: round(float(x))
        index = [list(map(rf,(i[0].split(","))))
                        for i in data.items()]
        # extremes
        smin = np.apply_along_axis( min,
                        axis=0, arr=np.asarray(index) )
        smax = np.apply_along_axis( max,
                        axis=0, arr=np.asarray(index) )
        # grid array
        grid = np.zeros(list((smax - smin + 1)))

        # fill grid
        for count, value in enumerate(index):
                # get coordinates
                idx = value - smin
                # save second rank order
                grid[tuple(idx)] = order[count]

        return grid, smin

def grd4smooth(grid, sigma):
        """KDE this OpenDX"""
        return gaussian_filter(grid, sigma,
                        mode='wrap',
                        output='float64',
                        truncate=8.0)

def grd2dx(grid, origin):
        """Comments
        origin represents
        the cartesian coordinates of 
        the center of the grid cell
        """

        # nxn array with the length 
        # of a grid cell along each axis
        delta  = np.zeros([3,3])
        np.fill_diagonal(delta, 1)

        # build an opendx grid
        dx = OpenDX.field('density')
        dx.add('positions', OpenDX.gridpositions(1, grid.shape, origin, delta))
        dx.add('connections', OpenDX.gridconnections(2, grid.shape))
        dx.add('data', OpenDX.array(3, grid))

        return dx

def dx4resample(name, factor):
        """Comments"""
        gddx = Grid()
        gddx.load(name)
        gddx.resample_factor(factor)
        gddx.export(name, file_format='dx')
