#!/usr/bin/env python3
# setup.py

from distutils.core import setup, Extension

colgraph_module = Extension('_libcolgraph', sources=['libcolgraph.i',
                                                     'Graph.cpp',
                                                     'Vertex.cpp'],
                             swig_opts=['-c++'],
                             extra_compile_args=['-std=gnu++11'])

setup(name='libcolgraph', ext_modules=[colgraph_module],
      py_modules=['libcolgraph'])
