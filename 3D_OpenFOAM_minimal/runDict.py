# MLMC_PORESCALE
# python3 software to generate random packings, CFD and statistical analysis
# -------------------------------------------------------------------------------------------
# AUTHOR: Matteo Icardi
# November 2013
#--------------------------------------------------------------------------------------------
# run.py script dictionary
# these global variables are used to select the correct modules to load

testcase = "testcase"
workdir  = "./"

#  ---  some general parameters applying for all modules (overwrite each module settings)
refratio       = 2         # refinement ratio between level (everything not set separately in ad-hoc functions) 
dimension      = 3         # problem dimensionality

#  --- NavierStokesOF, comp2phaseOF, incomp2phaseOF, darcyOF, discDarcyOF, transportOF, snappyOF, laplacianOF (openFOAM)
#  --- DarcyGG, DarcyDirGG, LaplacianGG, LaplacianDirGG (gmsh getdp)
#  --- none (packing problem)
pdeproblem = "NavierStokesOF"

#  --- geometry generation: bsand, random
packing    = "random"

#  --- type of study: mlmc, single
study     = "single"

# ----- type of run (pre,post,run,interactive,plot,multiple)
run = "setup"

# -----  output settings
plotformat = "png"

# ----- MULTIPLE MLMC estimation inputs
MLMCRealizations = 2
NTol = 3
TolVec = [0.1,0.05,0.025,0.01] #1/logspace(1,3,NTol)


#------- QUANTITY OF INTEREST (should return an array)
def final_qoi(result,geometry_object=None,solver_object=None):
    # result is a list of output
    # OpenFOAM:   for the full list of variables available in openfoam see the function qoi (line 297 in openfoam.py)
    # packing:    [porosity, ngrains, n_intersections, ntries_out]
    # Gmsh/Getdp: [porosity, flux, permeability, intvol, intout]

    # here you can do stuff with geometry and solver
    # e.g.,
    # geometry_object.write("gmsh",solver_object.name) to write geometry as gmsh format
    
    # The function has to return a list of QoI
    return [ i for i in result]
# ---------------------------------



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
