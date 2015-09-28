# MLMC_PORESCALE
# python3 software to generate random packings, CFD and statistical analysis
# -------------------------------------------------------------------------------------------
# AUTHOR: Matteo Icardi
# November 2013
#--------------------------------------------------------------------------------------------
# random.py dictionary for random packing inputs

use_stl    = True        # transform the geometry to STL first with OpenSCAD

#  --- grain packing settings
psd        = "uniform"    # grain size distribution (uniform, lognormal, constant)
coeffvar   = 0.4          # coefficient of variation of the grain size distribution
detached   = False        # overlapping or detached grains (required for GMSH)
jodreytory = True         # jodrey-tory algorithm
detachedbc = False        # overlapping or detached to the boundaries (required for GMSH)
ellips     = False         # using ellipsoids of spheres (only openfoam now)
minpor     = 0.5          # minimum porosity allowed   # THIS IS NOT WORKING PROPERLY
# BETTER TO FIX THE NUMBER OF GRAINS INSTEAD
mu         = 0.1          # mean grain size (overwritten if included in the MLMC hierarchy)
ngrains    = 1000         # total grain size (overwritten if included in the MLMC hierarchy)
max_tries  = 1e6          # number of tentatives to place randomly non-overlapping spheres
eps_jd     = 0.2          # jodrey-tory displacement (in overlapping distance units)
min_dist   = 1            # jodrey-tory distance threshold % (1=touching, <1 allow some overlap, >1 force distancing)
max_dist   = -1           # jodrey-tory distance threshold % (1=touching, <1 allow some overlap, >1 force distancing, <0 disabled)
cluster    = 3          # number of grains to consider for maximum distance
nmoves_jd  = 3          # number of grain to displace each JD iteration

#  --- domain settings
xlen      = 1.0          # length of the domain
ylen      = 1.0          # width of the domain
zlen      = 1.0          # depth of the domain
voidspace = 0.           # void space at the beginning and end of domain in x direction (mu units), set it to very small number if detachedbc is enable
dimension   = 3         # 2 or 3 dimensional simulations (overwritten by runDict)

# gmsh, openfoam, blender or none
geom_out="openscad"
workdir  = "./"  # overwritten by runDict



# ------------------------------------------------- END FILE


#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
