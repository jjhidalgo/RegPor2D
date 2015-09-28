# MLMC_PORESCALE
# python3 software to generate random packings, CFD and statistical analysis
# -------------------------------------------------------------------------------------------
# AUTHOR: Matteo Icardi
# November 2013
#--------------------------------------------------------------------------------------------
# general python script to run a MLMC example, plot and save the data

# -------------------------------
# ----- DO NOT CHANGE HERE
# ----- you can customize your run below
# -------------------------------

from runDefault import *

try:
    exec(open("runDict.py").read(),globals())
except IOError:
    print("Warning! file runDict.py not found or not readable. Loaded default values")

try:
    random
except:
    from general import *

import sys
sys.path.append("../")

import optparse

# check if the program is run with additional arguments
if len(sys.argv)>1:
    print("WARNING: program run with arguments, they may override the runDict dictionary")
    if ("help" in sys.argv[1]):
        print("For help please refer to the comments in the code and the README files")
        print("Command line arguments:\n runDict keywords (testcase, pde_problem, run, packing, study, plotformat) followed by their values")
        raise SystemExit
    for i in range(len(sys.argv))[1::2]:
        arg=sys.argv[i]
        if any([word in arg for word in["testcase","name"]]):
            testcase=sys.argv[i+1]
        elif any([word in arg for word in["pde","problem"]]):
            pde_problem=sys.argv[i+1]
        elif any([word in arg for word in["run","runmode", "runtype"]]):
            run=sys.argv[i+1]
        elif any([word in arg for word in["packing","geom"]]):
            packing=sys.argv[i+1]
        elif any([word in arg for word in["study"]]):
            study=sys.argv[i+1]
        elif any([word in arg for word in["plot","format"]]):
            plotformat=sys.argv[i+1]


# import the right study, geometry and solver modules
if (study=="mlmc"):
    import mlmc as stud
elif (study=="single"):
    import single as stud
else:
    print("ERROR, study type not found")
    raise SystemExit

if (packing=="random"):
    import randomgeo as geo
elif (packing=="bsand"):
    import bsand as geo
else:
    print("ERROR, packing type not found")
    raise SystemExit

if ("OF" in pdeproblem):
    import openfoam as sol
elif ("GG" in pdeproblem):
    import gmshgetdp as sol
else:
    print("WARNING, pdeproblem not recognized, running packing problem only")
    import packing as sol
    #raise SystemExit

# now there are 3 modules loaded: stud, geo and sol


# copy some important variables from one modules to others
sol.pdeproblem     = pdeproblem[:-2]
stud.geo_interface = geo.geom
stud.sol_interface = sol.solver
# TODO perform a check on some consistencies before starting


def main(runtype=run):
    random.seed()

    parser = optparse.OptionParser()
    parser.add_option('-l', '--logging-level', help='Logging level')
    parser.add_option('-f', '--logging-file', help='Logging file name')
    (options, args) = parser.parse_args()
    logging_level = LOGGING_LEVELS.get(options.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level, filename=options.logging_file,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')



# -------------------------------
# ----- DO NOT CHANGE ABOVE
# ----- you can customize your run now
# -------------------------------


    a=None
    if runtype=="run":
        t=time.time()
        # create the main object, called estimator
        a=stud.estimator(testcase,sol,geo)
        res=a.solve()
        print("Done! Elapsed Time: ", time.time()-t)
        print(res)
        try:
            a.save_qw()     # save the quantities of interest for each level and sample and the work loads for each level
            a.makeplot(plotformat)       # plotting function
        except:
            return res
    elif runtype=="setup":
        a=stud.estimator(testcase,sol,geo)
        res=a.generate()
    elif runtype=="pre":
        a=stud.estimator(testcase,sol,geo)
    elif runtype=="plot":
        stud.makeplot(None,None,testcase,plotformat)
    elif runtype=="post":
        a=stud.postprocess(testcase)
    else:
        print("No run specified. Please use command line or runDict properly")
    return a


# -------------------------------
# ----- DO NOT CHANGE BELOW
# -------------------------------


if __name__=='__main__':
    print("---------------------------------------")
    print("MLMC code for PDEs in random geometries")
    print("----------- GPL licensed --------------")
    print("please cite  Matteo Icardi et al., 2015")
    print("---------------------------------------")
    print("testcase: %s, study type: %s, run mode: %s, packing type: %s, plot format: %s" % (testcase,study,run,packing,plotformat))

    import multiprocessing
    #multiprocessing.set_start_method('forkserver') # fork, spawn, forkserver 
    main()
else:
    print("MLMC code run as a module")

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
