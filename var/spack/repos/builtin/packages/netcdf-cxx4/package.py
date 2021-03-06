# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetcdfCxx4(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C++ distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx4-4.3.1.tar.gz"

    maintainers = ['WardF']

    version('4.3.1', sha256='6a1189a181eed043b5859e15d5c080c30d0e107406fbb212c8fb9814e90f3445')
    version('4.3.0', sha256='e34fbc6aba243ec82c23e9ee99db2430555ada849c54c1f3ab081b0ddd0f5f30')

    # Usually the configure automatically inserts the pic flags, but we can
    # force its usage with this variant.
    variant('static', default=True, description='Enable building static libraries')
    variant('shared', default=True, description='Enable shared library')
    variant('pic', default=True, description='Produce position-independent code (for shared libs)')
    variant('dap', default=False, description='Enable DAP support')
    variant('jna', default=False, description='Enable JNA support')
    variant('doxygen', default=True, description='Enable doxygen docs')
    variant('ncgen4', default=True, description='Enable generating netcdf-4 data')
    variant('pnetcdf', default=True, description='Enable parallel-netcdf')
    variant('netcdf4', default=False, description='Enable netcdf-4 data structure')

    depends_on('netcdf-c')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')

    conflicts('~shared', when='~static')

    force_autoreconf = True

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.pic_flag)
        elif name == 'cppflags':
            flags.append('-I' + self.spec['netcdf-c'].prefix.include)

        return (None, None, flags)

    @property
    def libs(self):
        shared = True
        return find_libraries(
            'libnetcdf_c++4', root=self.prefix, shared=shared, recursive=True
        )

    def configure_args(self):
        config_args = []

        if '+static' in self.spec:
            config_args.append('--enable-static')
        else:
            config_args.append('--disable-static')

        if '+shared' in self.spec:
            config_args.append('--enable-shared')
        else:
            config_args.append('--disable-shared')

        if '+pic' in self.spec:
            config_args.append('--with-pic')
        else:
            config_args.append('--without-pic')

        if '+dap' in self.spec:
            config_args.append('--enable-dap')
        else:
            config_args.append('--disable-dap')

        if '+jna' in self.spec:
            config_args.append('--enable-jna')
        else:
            config_args.append('--disable-jna')

        if '+pnetcdf' in self.spec:
            config_args.append('--enable-pnetcdf')
        else:
            config_args.append('--disable-pnetcdf')

        if '+netcdf4' in self.spec:
            config_args.append('--enable-netcdf-4')
        else:
            config_args.append('--disable-netcdf-4')

        if '+ncgen4' in self.spec:
            config_args.append('--enable-ncgen4')
        else:
            config_args.append('--disable-ncgen4')

        if '+doxygen' in self.spec:
            config_args.append('--enable-doxygen')
        else:
            config_args.append('--disable-doxygen')

        return config_args
