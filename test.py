# Test for RegPore2D.

from RegPore2D import RegPore2D as rp
a = rp(nx=23,ny=23,radius=0.02,packing='tri')
b = rp(nx=11,ny=11,radius=0.04,packing='tri',xoffset = 1.0)

c = a+b

a.write_mesh(fname='a.geo', meshtype='gmsh')
b.write_mesh(fname='b.geo', meshtype='gmsh')
c.write_mesh(fname='c.geo', meshtype='gmsh')
c.write_mesh(fname='c.scad', meshtype='oscad')
