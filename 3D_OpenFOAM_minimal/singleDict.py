# MLMC_PORESCALE
# python3 software to generate random packings, CFD and statistical analysis
# -------------------------------------------------------------------------------------------
# AUTHOR: Matteo Icardi
# November 2013
#--------------------------------------------------------------------------------------------
# single.py dictionary

#  --- simulation settings
cleardat = False        # for big simulations, this clear the final CFD data to save space
#nprocs   = 1            # number of processes for openfoam solver, or keywork "max"
nthreads = "adaptive"   # max number of threads for parallel sampling, or keyword "adaptive"
writelog = True

refratio = 1            # not used for single simulations

#------- HIERARCHY DEFINITTION ROUTINE
#  --- SOLVER TOLERANCE
def get_tol(level):
    t=tol0*pow(1.5,-level)
    return t

#  --- MEAN GRAIN SIZE
def get_mean(level):
    m=mu0*pow(2.0,-level*2*third)#0.2*pow(2.0,-level*third)
    return m

#  --- NUMBER OF GRAINS
def get_n(level):
    n = n0*(level+1)#pow(2,level)
    return n

#  --- DOMAIN SIZE SCALING
def get_len(level):
    n = pow(2,level)
    return n
# ---------------------------------

#  --- GEOMETRY ITERATIONS
def get_max_tries(level):
    n = pow(2,level+4)
    return n




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
