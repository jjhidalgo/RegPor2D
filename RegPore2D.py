import numpy as np
import PoreError as PoreError
class RegPore2D:
    """Regular 2D rectangular porous medium
       Ly (height) is always 1. Pore throat and Lx (length)
        are computed according to the packing."""

    global CONST_ZETA # z coordinate of all points.
    CONST_ZETA = 0.5
#
#-----------------------------------------------------------------------
#
    def __init__(self,nx=2,ny=2,radius=0.1,xoffset=0.0,packing='sqr'):
        """Checks arguments and creates the packing of discs."""

        self.__packs = ['tri', 'sqr', 'etri']
        self.radius = None
        self.throat = None
        self.nx = None
        self.ny = None
        self.circles = None
        self.xoffset = 0.0
        self.Ly = 1.0

        if self.checkPacking(packing):
           self.packing = packing
        else:
           raise PoreError.ErrorPacking


        if self.checkRadius(radius):
            self.radius = radius
        else:
            raise PoreError.ErrorRadius

        if self.checkNx(nx):
            self.nx = nx
        else:
            raise PoreError.ErrorNx

        if self.checkNy(ny):
            self.ny = ny
        else:
            raise PoreError.ErrorNy

        self.throat = self.__ComputeThroat__()

        if self.throat < 1.e-9:
           raise PoreError.ErrorThroatNegative

        self.Lx = self.__ComputeLx__()


        self.GeneratePacking()

#
#-----------------------------------------------------------------------
#
    def checkPacking(self,packing):
        """Checks if the packing is valid
        The only alowwed packings are:
            tri -- triangular
            sqr  -- square
            etri -- elongated triangular
        """

        if packing in self.__packs:
           packOK = True
        else:
           packOK = False

        return packOK
#
#-----------------------------------------------------------------------
#
    def checkNx(self,nx):
        """Checks if the number of grains in the x direcction
           is positive."""

        NxOK = False

        if nx > 0:
            if (self.packing != 'sqr' and nx % 2 != 0) \
               or self.packing == 'sqr':
              NxOK = True
        
        return NxOK
#
#-----------------------------------------------------------------------
#
    def checkNy(self,ny):
        """Checks if the number of grains in the y direcction
           is positive and that ny*radius<1.0."""

        if ny>0 or self.radius*ny < 1.0:
           NyOK = True
        else:
           NyOK = False

        return NyOK
#
#-----------------------------------------------------------------------
#
    def checkRadius(self,radius):
        """Checks if the grain radius is greater than 1.0e-9"""

        if radius > 1.0e-9 and self.radius < self.Ly:
           RadiusOK = True
        else:
           RadiusOK = False

        return RadiusOK

#
#-----------------------------------------------------------------------
#
    def __ComputeLx__(self):
        """Computes the lenght of the system in the x
           direction according to the packing and the geometry"""

        if self.packing == 'tri' or self.packing == 'etri':
            Lx = ((3.0*self.nx + 1.0)*self.throat
                + 2.0*self.radius*(2.0*self.nx+1.0))

        elif self.packing=='sqr':
            Lx = ((self.nx + 1.0)*self.throat
                + 2.0*self.nx*self.radius)

        return Lx

#
#-----------------------------------------------------------------------
#
    def __ComputeThroat__(self):
        """Computes throat from ny, Ly, and radius"""

        throat = (self.Ly - (2.0*self.ny*self.radius))/(self.ny + 1)
        return throat

#
#-----------------------------------------------------------------------
#
    def GeneratePacking(self):
        """ Generates the position of the grains"""

        if self.packing == 'tri':
            self.circles = self.PackTri()

        elif self.packing=='sqr':
            self.circles = self.PackSqr()

        elif self.packing == 'etri':
            self.circles = self.PackEtri()
#
#-----------------------------------------------------------------------
#

    def PackSqr(self):
        """ Generates the coordinates of the grain centers
            for the square packing"""

        i = np.arange(1,self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j = np.arange(1,self.ny + 1)
        yj = j*self.throat + (2.0*j -1.0)*self.radius


        ngrains = self.nx*self.ny
        circles = np.zeros(ngrains,
                       dtype={'names':['x','y','z','r'],
                              'formats':['f4','f4','f4','f4']})


        circles[:]['x'] = xi.repeat(self.ny) + self.xoffset
        circles[:]['y'] = np.tile(yj,self.nx)
        circles[:]['z'] = np.tile(CONST_ZETA,ngrains)
        circles[:]['r'] = np.tile(self.radius,ngrains)


        return circles

#
#-----------------------------------------------------------------------
#
    def PackTri(self):
        """ Generates the coordinates of the grain centers
            for the tri packing"""

        i = np.arange(1,self.nx + 1)
        xi =  i*self.throat + (2.0*i -1.0)*self.radius

        j_odd = np.arange(1,self.ny+1)
        yj_odd = j_odd*self.throat + (2.0*j_odd -1.0)*self.radius

        j_even = np.arange(1,self.ny)
        yj_even = j_even*(self.throat + 2.0*self.radius) + self.throat/2.0
        yj = np.hstack((yj_odd,yj_even))
        

        xrep = np.ones(self.nx,dtype=np.int)
        xrep[::2] = self.ny*xrep[::2] #odd
        xrep[1::2] = (self.ny-1)*xrep[1::2] #even

        ngrains = (self.nx/2)*(self.ny-1)+ (self.nx/2+1)*(self.ny)
        circles = np.zeros(ngrains,
                           dtype={'names':['x','y','z','r'],
                                  'formats':['f4','f4','f4','f4']})


        circles[:]['x'] = xi.repeat(xrep) + self.xoffset
        circles[:]['y'] = np.hstack((np.tile(yj,self.nx/2),yj_odd))
        circles[:]['z'] = np.tile(CONST_ZETA,ngrains)
        circles[:]['r'] = np.tile(self.radius,ngrains)


        return circles
#
#-----------------------------------------------------------------------
#

    def PackEtri(self):
        """ Generates the coordinates of the grains' centers
            for the elongated triangular packing"""

        i = np.arange(1,self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j = np.arange(1,self.ny + 1)
        yj = j*self.throat + (2.0*j -1.0)*self.radius


        ngrains = self.nx*self.ny
        circles = np.zeros(ngrains,
                       dtype={'names':['x','y','z','r'],
                              'formats':['f4','f4','f4','f4']})


        circles[:]['x'] = xi.repeat(self.ny) + self.xoffset
        circles[:]['y'] = np.tile(yj,self.nx)
        circles[:]['z'] = np.tile(CONST_ZETA,ngrains)
        circles[:]['r'] = np.tile(self.radius,ngrains)


        return circles

#
#-----------------------------------------------------------------------
#

    def __add__(self,other):
        """Joins two porous media"""

        dist = np.abs((self.radius+self.offset) - (other.radius+other.offsett))
        d2 =np.abs(self.radius -other.radius)

        if dist < d2:
            raise PoreError.ErrorOverlap
        else:

            # Creates a dummy pore medium
            NewPore = RegPore2d(self,nx=2,ny=2,radius=0.1,packing='sqr')

            ngrains = self.circles.shape[0] + self.circles.shape[0]

            newcircles = np.zeros(ngrains,
                               dtype={'names':['x','y','r'],
                                      'formats':['f4','f4','f4']})

            newcircles[:]['x'] = np.concatenate((self.circles['x'],
                                              other.circles['x']),axis=0)

            newcircles[:]['y'] = np.concatenate((self.circles['y'],
                                              other.circles['y']),axis=0)
            newcircles[:]['r'] = np.concatenate((self.circles['r'],
                                              other.circles['r']),axis=0)

            NewPore.circles = newcircles

            return NewPore

#
#-----------------------------------------------------------------------
#
    def write_mesh(self,fname='untitled.geo',meshtype='gmsh'):
        """ Writes the porus media for the mesh/cad program"""
        meshes = {'gmsh':self.__writeGMSH__,'scad':self.__writeSCAD__}
        try:
            meshes[meshtype](fname)
        except:
            print("Unknown meshtype")
            

        #self.__writeGMSH__(fname)


#
#-----------------------------------------------------------------------
#
    def __writeGMSH__(self,fname='untitled.geo'):
        """Writes the discs packing for gmsh"""

        import PyGmsh as gmsh
        from PyGmsh import gmshPoint as gpt

        mesh = gmsh.PyGmsh()

        xmin = np.min(self.circles[:]['x']) - self.radius - self.throat
        xmax = np.max(self.circles[:]['x']) + self.radius + self.throat
        ymin = np.min(self.circles[:]['y']) - self.radius - self.throat
        ymax = np.max(self.circles[:]['y']) + self.radius + self.throat
        z = CONST_ZETA
        size = ymax/10.

        mesh.add_BoundingBox(xmin,xmax,ymin,ymax,z,size)

        for circ in self.circles:

            center = (circ['x'],circ['y'],circ['z'])
            r = circ['r']
            mesh.add_circle(center,r,r/10.)


        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
#
    def __writeSCAD__(self,fname='untitled.scad'):
        """Writes the discs packing for SCAD"""
        
        print("Not implemented yet!")
#
#-----------------------------------------------------------------------
# END class RegPore2D
#-----------------------------------------------------------------------
#
