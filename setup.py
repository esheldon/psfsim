import os
import distutils
from distutils.core import setup, Extension, Command
import numpy

scripts=['psfsim-make-scripts']

scripts=[os.path.join('bin',s) for s in scripts]

setup(
    name="psfsim", 
    packages=['psfsim'],
    scripts=scripts,
    version="0.1",
)




