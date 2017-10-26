##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install parflow
#
# You can edit this file again by typing:
#
#     spack edit parflow
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import sys


class Parflow(CMakePackage):
    """ParFlow is an open-source parallel watershed model."""

    homepage = "https://www.parflow.org/"
    url      = "https://github.com/parflow/parflow/archive/v3.2.1.tar.gz"

    # FIXME: Add proper versions and checksums here.
    version('develop', git='https://github.com/parflow/parflow.git', branch='master')
    version('3.2.1', '5454efe36170eb23c7c95fbe8ffe76db')

    # Using explicit versions to keep builds consistent
    depends_on('tcl@8.6.6')

    depends_on('mpi@3.0.0')
    
    depends_on('hdf5@1.10.1 +mpi')
    depends_on('netcdf@4.4.1.1')
    depends_on('parallel-netcdf@1.8.0')
    depends_on('silo@4.10.2 -hzip -fpzip')

    depends_on('hypre@2.12.1')

    parallel = False

    def cmake_args(self):
        """Populate cmake arguments for ParFlow."""
        spec = self.spec

        if sys.platform == 'darwin':
                shared_suffix = 'dylib'
        else:
            shared_suffix = 'so'

        cmake_args = [
            '-DPARFLOW_AMPS_LAYER=mpi1',
            '-DTCL_TCLSH={0}/tclsh'.format(spec['tcl'].prefix.bin),
            '-DTCL_LIBRARY={0}/libtcl8.6.{1}'.format(spec['tcl'].prefix.lib, shared_suffix),
            '-DHDF5_ROOT={0}'.format(spec['hdf5'].prefix),
            '-DSILO_ROOT={0}'.format(spec['silo'].prefix),
            '-DHYPRE_ROOT={0}'.format(spec['hypre'].prefix),
            '-DNETCDF_DIR={0}'.format(spec['netcdf'].prefix),
            '-DPARFLOW_HAVE_CLM=TRUE',
            '-DPARFLOW_AMPS_LAYER=mpi1',
            '-DPARFLOW_AMPS_SEQUENTIAL_IO=true',
        ]

        return cmake_args
