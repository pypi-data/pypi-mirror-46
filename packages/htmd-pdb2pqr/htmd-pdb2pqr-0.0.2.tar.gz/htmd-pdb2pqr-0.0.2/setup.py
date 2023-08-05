import setuptools
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os

setup(name='htmd-pdb2pqr',
      version='0.0.2',
      url='http://www.poissonboltzmann.org/',
      description="PDB2PQR: an automated pipeline for the setup of Poisson-Boltzmann electrostatics calculations",
      long_description="""
pdb2pqr
============

This directory is the home for the [PDB2PQR software](http://www.poissonboltzmann.org/docs/structures-ready/). 

Some useful information:
* See the [install notes](INSTALL.md) to build pdb2pqr.
* Using pdb2pqr [binaries](BINARY_README.md)
* Latest [changelog](ChangeLog.md)
* For testing the [server](ServerNotes.md) (for developers)


Please see the [user guide](http://www.poissonboltzmann.org/docs/pdb2pqr-algorithm-description/) for documentation and the [COPYING file](COPYING) for license information.

Please see [programmer's guide](http://www.poissonboltzmann.org/docs/pdb2pqr-programmers/) for information on working with the PDB2PQR code. 
""",
      license="BSD",
      packages=['pdb2pqr',
                'pdb2pqr.src',
                'pdb2pqr.pdb2pka',
                'pdb2pqr.propka30',
                'pdb2pqr.extensions'
                ],
      package_data={'pdb2pqr': ['dat/*', 'NEWS', 'README.md', 'COPYING', 'AUTHORS']},
      cmdclass=dict(build_py=build_py),
      entry_points={
          'console_scripts': [
              'pdb2pqr_cli = pdb2pqr.main:main'
          ]
      }
      )
