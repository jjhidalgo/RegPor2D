# Test for REgPore2D.

from RegPore2D import RegPore2D as rp
a = rp(nx=41,ny=34,radius=0.01,packing='tri')
a.write_mesh()
