"""2D rectangular poroues medium generation"""

import numpy as np
import warnings
import PoreError as PoreError
class RegPore2D(object):
    """Regular 2D rectangular porous medium
       ly (height) is always 1. Pore throat and Lx (length)
        are computed according to the packing."""

    global CONST_ZETA # z coordinate of all points.
    CONST_ZETA = 0.5
#
#-----------------------------------------------------------------------
#
    def __init__(self, nx=2, ny=2, radius=0.1, xoffset=0.0, packing='sqr'):
        """Checks arguments and creates the packing of discs."""

        self.__packs = ['tri', 'sqr', 'etri']
        self.radius = None
        self.throat = None
        self.nx = None
        self.ny = None
        self.ngrains = None
        self.circles = None
        self.xoffset = xoffset
        self.ly = 1.0

        if self.check_packing(packing):
            self.packing = packing
        else:
            raise PoreError.ErrorPacking


        if self.check_radius(radius):
            self.radius = radius
        else:
            raise PoreError.ErrorRadius

        if self.check_nx(nx):
            self.nx = nx
        else:
            raise PoreError.ErrorNx

        if self.check_ny(ny):
            self.ny = ny
        else:
            raise PoreError.ErrorNy

        self.throat = self.__compute_throat__()

        if self.throat < 1.e-9:
            raise PoreError.ErrorThroatNegative

        self.Lx = self.__compute_lx__()

        self.ngrains = self.__ngrains__()

        self.size = 0.8*self.throat

        self.generate_packing()

#
#-----------------------------------------------------------------------
#
    def check_packing(self, packing):
        """Checks if the packing is valid
        The only alowwed packings are:
            tri -- triangular
            sqr  -- square
            etri -- elongated triangular
        """

        if packing in self.__packs:
            pack_ok = True
        else:
            pack_ok = False

        return pack_ok
#
#-----------------------------------------------------------------------
#
    def check_nx(self, nx):
        """Checks if the number of grains in the x direcction
           is positive."""

        nx_ok = False

        if nx > 0:
            if (self.packing != 'sqr' and nx % 2 != 0) \
                or self.packing == 'sqr':
                nx_ok = True

        return nx_ok
#
#-----------------------------------------------------------------------
#
    def check_ny(self, ny):
        """Checks if the number of grains in the y direcction
           is positive and that ny*radius<1.0."""

        if ny > 0 or self.radius*ny < 1.0:
            ny_ok = True
        else:
            ny_ok = False

        return ny_ok
#
#-----------------------------------------------------------------------
#
    def check_radius(self, radius):
        """Checks if the grain radius is greater than 1.0e-9"""

        if radius > 1.0e-9 and self.radius < self.ly:
            radius_ok = True
        else:
            radius_ok = False

        return radius_ok

#
#-----------------------------------------------------------------------
#
    def __compute_lx__(self):
        """Computes the lenght of the system in the x
           direction according to the packing and the geometry"""

        if self.packing == 'tri' or self.packing == 'etri':
            lx = (3.0*self.nx + 1.0)*self.throat \
                + 2.0*self.radius*(2.0*self.nx+1.0)

        elif self.packing == 'sqr':
            lx = (self.nx + 1.0)*self.throat \
                + 2.0*self.nx*self.radius

        return lx

#
#-----------------------------------------------------------------------
#
    def __compute_throat__(self):
        """Computes throat from ny, ly, and radius"""

        throat = (self.ly - (2.0*self.ny*self.radius))/(self.ny + 1)
        return throat
#
#-----------------------------------------------------------------------
#
    def set_size(self, size):
        """Sets mesh size and generares packing, again."""
        #TO DO: check input argument. Allow a general
        # expression using, x, y, r.

        self.size = size
        self.generate_packing()

#
#-----------------------------------------------------------------------
#
    def generate_packing(self):
        """ Generates the position of the grains"""

        if self.packing == 'tri':
            self.circles = self.pack_tri()

        elif self.packing == 'sqr':
            self.circles = self.pack_sqr()

        elif self.packing == 'etri':
            self.circles = self.pack_etri()
#
#-----------------------------------------------------------------------
#

    def pack_sqr(self):
        """ Generates the coordinates of the grain centers
            for the square packing"""

        global CONST_ZETA

        i = np.arange(1, self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j = np.arange(1, self.ny + 1)
        yj = j*self.throat + (2.0*j -1.0)*self.radius


        circles = np.zeros(self.ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})


        circles[:]['x'] = xi.repeat(self.ny) + self.xoffset
        circles[:]['y'] = np.tile(yj, self.nx)
        circles[:]['z'] = np.tile(CONST_ZETA, self.ngrains)
        circles[:]['r'] = np.tile(self.radius, self.ngrains)

        return circles

#
#-----------------------------------------------------------------------
#
    def pack_tri(self):
        """ Generates the coordinates of the grain centers
            for the tri packing"""

        #global CONST_ZETA

        i = np.arange(1, self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j_odd = np.arange(1, self.ny+1)
        yj_odd = j_odd*self.throat + (2.0*j_odd -1.0)*self.radius

        j_even = np.arange(1, self.ny)
        yj_even = j_even*(self.throat + 2.0*self.radius) + self.throat/2.0
        yj = np.hstack((yj_odd, yj_even))


        xrep = np.ones(self.nx, dtype=np.int)
        xrep[::2] = self.ny*xrep[::2] #odd
        xrep[1::2] = (self.ny-1)*xrep[1::2] #even

        circles = np.zeros(self.ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})


        circles[:]['x'] = xi.repeat(xrep) + self.xoffset
        circles[:]['y'] = np.hstack((np.tile(yj, self.nx/2), yj_odd))
        circles[:]['z'] = np.tile(CONST_ZETA, self.ngrains)
        circles[:]['r'] = np.tile(self.radius, self.ngrains)


        return circles
#
#-----------------------------------------------------------------------
#

    def pack_etri(self):
        """ Generates the coordinates of the grains' centers
            for the elongated triangular packing"""

        global CONST_ZETA

        i = np.arange(1, self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j = np.arange(1, self.ny + 1)
        yj = j*self.throat + (2.0*j -1.0)*self.radius


        circles = np.zeros(self.ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})


        circles[:]['x'] = xi.repeat(self.ny) + self.xoffset
        circles[:]['y'] = np.tile(yj, self.nx)
        circles[:]['z'] = np.tile(CONST_ZETA, self.ngrains)
        circles[:]['r'] = np.tile(self.radius, self.ngrains)


        return circles

#
#-----------------------------------------------------------------------
#

    def __add__(self, other):
        """Joins two porous media."""

        # Checks if other is a porous medium
        if other.__class__.__name__ != 'RegPore2D':
            raise PoreError.ErrorNotPorousMedium

        # Warns user if porous media overlap.
        if self.__overlap__(other):
            warnings.warn('Porous media overlap')


        new_pore = self.__class__()
        new_pore.ngrains = self.ngrains + other.ngrains

        newcircles = np.zeros(new_pore.ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})

        newcircles[:]['x'] = np.concatenate((self.circles['x'], \
                                            other.circles['x']), axis=0)

        newcircles[:]['y'] = np.concatenate((self.circles['y'], \
            other.circles['y']), axis=0)

        newcircles[:]['z'] = np.concatenate((self.circles['z'], \
            other.circles['z']), axis=0)

        newcircles[:]['r'] = np.concatenate((self.circles['r'], \
            other.circles['r']), axis=0)

        new_pore.circles = newcircles
        new_pore.throat = min([self.throat, other.throat])
        new_pore.size = min([self.size, other.size])

        return new_pore
#
#-----------------------------------------------------------------------
#

    def __ngrains__(self):
        """Computes number of grians according to the packing"""

        if (self.packing == 'sqr') | (self.packing == 'etri'):
            ngrains = self.nx*self.ny

        else:
            ngrains = (self.nx/2)*(self.ny-1)+ (self.nx/2+1)*(self.ny)

        return ngrains

#
#-----------------------------------------------------------------------
#

    def __overlap__(self, other):
        """Checks if two porous media overlap."""

        if other.__class__.__name__ != 'RegPore2D':
            raise PoreError.ErrorNotPorousMedium

        a_x1 = np.min(self.circles['x'])
        a_x2 = np.max(self.circles['x'])
        a_y1 = np.min(self.circles['y'])
        a_y2 = np.max(self.circles['y'])

        b_x1 = np.min(other.circles['x'])
        b_x2 = np.max(other.circles['x'])
        b_y1 = np.min(other.circles['y'])
        b_y2 = np.max(other.circles['y'])

        overlap = not((a_x1 > b_x2) or \
            (a_x2 < b_x1) or \
            (a_y2 < b_y1) or \
            (a_y1 > b_y2))

        return overlap
#
#-----------------------------------------------------------------------
#
    def write_mesh(self, fname='', meshtype='gmsh'):
        """ Writes the porus media for the mesh/cad program"""
        meshes = {'gmsh':self.__writeGMSH__, 'oscad':self.__writeOPENSCAD__}

        meshes[meshtype](fname)
#
#-----------------------------------------------------------------------
#
    def __writeGMSH__(self, fname):
        """Writes the discs packing for gmsh"""

        import PyGmsh as gmsh
        global CONST_ZETA

        mesh = gmsh.PyGmsh()

        xmin = np.min(self.circles[:]['x'] - self.circles[:]['r']) - self.throat
        xmax = np.max(self.circles[:]['x'] + self.circles[:]['r']) + self.throat
        ymin = np.min(self.circles[:]['y'] - self.circles[:]['r']) - self.throat
        ymax = np.max(self.circles[:]['y'] + self.circles[:]['r']) + self.throat
        z = CONST_ZETA
        size = self.size

        mesh.add_BoundingBox(xmin, xmax, ymin, ymax, z, size)

        for circ in self.circles:

            center = (circ['x'], circ['y'], circ['z'])
            r = circ['r']
            mesh.add_circle(center, r, size)

        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
#
    def __writeOPENSCAD__(self, fname):
        """Writes the discs packing for OpenSCAD"""

        import PyOpenSCAD as oscad
        global CONST_ZETA

        z = CONST_ZETA

        mesh = oscad.PyOpenSCAD()


        for circ in self.circles:

            center = (circ['x'], circ['y'], circ['z'])
            r = circ['r']
            mesh.add_cylinder(z, r, center)


        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
# END class RegPore2D
#-----------------------------------------------------------------------
#
