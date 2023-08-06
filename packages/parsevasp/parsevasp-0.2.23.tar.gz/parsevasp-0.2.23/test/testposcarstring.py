#!/usr/bin/python
import sys
import io
import os
import logging
import numpy as np
testdir = os.path.dirname(__file__)
srcdir = '../parsevasp'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import vasprun

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Testing')

vasprun = vasprun.Xml(file_path='basic.xml')

print vasprun.get_structure()

# poscar.modify("unitcell", np.array([[2.0, 0.0, 0.0],
#                                    [0.0, 2.0, 0.0],
#                                    [0.0, 0.0, 2.0]]))
# poscar.delete_site(3)

#poscar.write(file_path=testdir + "/POSCARMOD")
