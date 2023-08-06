# -*- Mode: python
#
# Licenses 
# Authors

"""\
Extend Core TopologyGroup object with method srank
==================================================

Comments

Classes
-------

.. _srankSlow

Helper functions
----------------

.. angle

"""

###########################################################################
#### imports                                                              #
###########################################################################

import numpy as np

from math import atan2
from MDAnalysis.lib import mdamath
from MDAnalysis.lib.distances import apply_PBC
from MDAnalysis.core.topologyobjects import TopologyGroup

###########################################################################
#### functions / classses                                                 #
###########################################################################

# this is a slow function
def _angle(x, y):
	"""
	Calculate angle between two vectors
	return value in the range [-pi:pi]
	"""
	d = np.dot(x,y)
	n = mdamath.norm(np.cross(x,y))
	return atan2(n,d)

# point of this class
def _srankSlow(self, pbc=False):
	"""
	Calculate the internal product between bond vector and z-axis.	
	The z-axis is defined here as (0,0,1) by default
	
	Parameters
	----------
	self: object
	    TopologyGroup where each element correspond to the coordinate
	    of a tuple of atoms belonging to a bond type

	pbc : bool
	    apply periodic boundary conditions when calculating bond vectors
	    this is important when connecting vectors between atoms might 
	    require minimum image convention
	
	Returns
	-------
	cosine square : ndarray
	
	"""
	if not self.btype == 'bond':
		raise TypeError("TopologyGroup is not of type 'bond'")
	
	# define z vector
	z = np.array([0, 0 ,1])	

	if pbc:
		# box dimensions
		box = self._ags[0].dimensions
		# get positions of atoms to primary box
		a = apply_PBC(self._ags[0].positions, box)
		b = apply_PBC(self._ags[1].positions, box)
		# calculate bond vector for all pair of atoms
		v = b - a
		# calculate angle for all bonds
		ang = np.array([_angle(i,z) for i in v])
		# return angle
		return ang
	else:
		v = self._ags[1].positions - self._ags[0].positions
		ang = np.array([_angle(i,z) for i in v])
		return ang
	
# add the method to the class
TopologyGroup._srankSlow = _srankSlow

