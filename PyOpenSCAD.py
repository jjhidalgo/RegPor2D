import numpy as np

class PyOpenSCAD:
    """OenSCAD wrapper."""

    global _id_Cubes
    global _id_Cylinders
    global _id_Spheres

    _id_Cubes = 0
    _id_Cylinders = 0
    _id_Spheres = 0
#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """Just creates empty arrays"""
        
        self.Cubes = []
        self.Cylinders = []
        self.Spheres = []


#
#-----------------------------------------------------------------------
#
    def add_cylinder(self,height,radius,center=None):
        """" Adds one cylinder to the mesh."""
        from PyOpenSCAD import oscadCylinder as oc

        cylinder = oc(height,radius,center)
        self.Cylinders.append(cylinder)

        return cylinder

#
#-----------------------------------------------------------------------
#
    def add_sphere(self,radius,center=None):
        """" Adds one sphere to the mesh."""
        from PyOpenSCAD import oscadSphere as osph

        sphere = osph(radius,size,center)
        self.Spheres.append(sphere)

        return sphere
#
#-----------------------------------------------------------------------
#
    def add_cube(self,size,center=None):
        """" Adds one cube to the mesh."""
        from PyOpenSCAD import oscadCube as ocube

        cube = ocube(size,center)
        self.Cubes.append(cube)

        return cube
#
#-----------------------------------------------------------------------
#
    def write_code(self,fname):
        """Writes the mesh in OpenScad format."""
        oscad_code = [""]
        
        for sphere in self.Spheres:
            
            oscad_code.append(sphere.code())

        for cylinder in self.Cylinders:
            oscad_code.append(cylinder.code())

        for cube in self.Cubes:
            oscad_code.append(cube.code())

        if fname=='':
            fname = 'untitled.scad'
            
        geo_file = open(fname, "w")
        geo_file.write(''.join(oscad_code))
        geo_file.close()

#
#-----------------------------------------------------------------------
# END class PyOpenSCAD
#-----------------------------------------------------------------------
#
class oscadObject:
    """This class creates a generic openSCAD object.
       (limited to cubes, spheres, cylinders or polygons)"""

#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """To be redefined in children."""
        pass        

#
#-----------------------------------------------------------------------
#
    def code(self,):
        """To be redefined in children."""
        pass        

#
#-----------------------------------------------------------------------
#
    def translate_code(self,code_in):
        """Wrapps code in a translate environment."""

        center = ','.join(map(str,self.center))

        code = 'translate([{:}])'.format(center)
        code += code_in

        return code


#
#-----------------------------------------------------------------------
# END class oscadObject
#-----------------------------------------------------------------------
#

class oscadCylinder(oscadObject):
    """This class creates and writes code for a cylinder in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self,height,radius,center=None):
        """Creates a cylinder."""
        
        self.height = height 
        self.radius = radius
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cylinder openSCAD format."""
        
        cylinder_code = 'cylinder(h={:.9f},r={:.9f})'.format(
                                      self.height,self.radius)

        if self.center != None:
            cylinder_code = self.translate_code(cylinder_code)
            
        return cylinder_code + '; \n'

#
#-----------------------------------------------------------------------
# END class oscadCylinder
#-----------------------------------------------------------------------
#


class oscadSphere(oscadObject):
    """This class creates and writes code for a sphere in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self,radius,center=None):
        """Creates a sphere."""
        
        self.radius = radius
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a sphere openSCAD format."""
        
        sphere_code = 'sphere(r={:.9f})'.format(self.radius)

        if self.center != None:
            sphere_code = self.translate_code(sphere_code)
            
        return sphere_code + '; \n'

#
#-----------------------------------------------------------------------
# END class oscadSphere
#-----------------------------------------------------------------------
#


class oscadSphere(oscadObject):
    """This class creates and writes code for a sphere in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self,size,center=None):
        """Creates a cube."""
        
        self.size = size 
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cube in openSCAD format."""
        
        cube_code = 'cube(size={:.9f})'.format(self.size)

        if self.center != None:
            cube_code = self.translate_code(cube_code)
            
        return cube_code + '; \n'

#
#-----------------------------------------------------------------------
# END class oscadCube
#-----------------------------------------------------------------------
#
