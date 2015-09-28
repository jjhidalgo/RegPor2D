# MLMC_PORESCALE
# python3 software to generate random packings, CFD and statistical analysis
# -------------------------------------------------------------------------------------------
# AUTHOR: Matteo Icardi and Gianluca Boccardo
# March 2015
#--------------------------------------------------------------------------------------------
# bsand.py dictionary

# WARNING: when using BSAND, also the randomgeoDict dictionary is loaded.
# These are extra setting only for BSand

#  --- domain settings
###Container Specification
container           = "cyl" # "box" for a box, "cyl" for a cylinder. 
box_extra_length   = 0.2    # box is increased in all directions to avoid simulating fluid close to the wall
cyl_extra_height   = 0.2    # cyl is increased only in height to reduce inlet-outlet effect
measure_volume     = 0.9    # cyl and box are reduced to compute post processing porosity (between 0 and 1)


### Object Specification
#non_primitive_model=
#Options: 0 deactivated (spheres), "filename" for a filename.blend model, to be found in a ./Library subfolder
non_primitive_model = 0
randomize_grains    = 0      #TODO 
deposition          = True   # run the deposition simulation
postprocess         = True   # compute porosity and other postprocessing
refine_level        = 1      # refinement level for blender ico-spheres
grain_rescale       = 0.9    # rescaling after the deposition simulation, between 0 and 1
remove_grain        = False  # remove grain with fallen outside
update_grain        = False  # update the original grain position

# function to adapt the rescaling to the refinement level
def set_grain_rescale(level):
    return 1-(1-grain_rescale)*2**(-level)

# functions to speed up the simulation based on the level
def set_niter(level):
    return (level+1)*2
def set_nsteps(level):
    return 100 #(level+1)*30

### Physical simulation parameters
linear_damping  = 0.99    # between 0 and 1
angular_damping = 1.0     # between 0 and 1
friction        = 0.5     # between 0 and 1
restitution     = 0.      # between 0 and 1
gravity         = -10.0   # gravity
mean_mass       = 1000    # mass of a mean size particle (ATTENTION: Blender can not handle object mass smaller then 0.001)
margin          = 0.0     # collision margin, between 0 and 1 (>0 to allow overlapping)
btime           = 20      # blender time / physical time
autotime        = False   # compute total simulation time based automatically
max_time        = 400     # manual selection of total simulation time 
relax_time      = 0.01    # relax time after falling per unit mass per unit velocity
deposition_height = 1     # stretching factor to facilitate the initial random placement
deposition_shift  = 0     # shifting factor to let the grain start from a non-zero height


### Other parameters
write_blender_file = False  # write all steps
write_final_file   = False  # write only one final blender file


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
