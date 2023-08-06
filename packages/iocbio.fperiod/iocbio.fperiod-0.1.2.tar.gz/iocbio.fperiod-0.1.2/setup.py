#!/usr/bin/env python3

import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("iocbio.fperiod",
              sources=["iocbio/fperiod.pyx", "src/libfperiod.c"],
              libraries=["m"], # Unix-like specific
              language="c",
              include_dirs = [numpy.get_include(), "src"],
              extra_compile_args = ["-funroll-loops"],
          )
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='iocbio.fperiod',
      version='0.1.2',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='IOCBio FPeriod',
      author='IOCBio team',
      author_email='iocbio@sysbio.ioc.ee',
      license='BSD',
      url='https://gitlab.com/iocbio/fperiod',
      ext_modules=cythonize(ext_modules),
      install_requires=[
          'numpy',
          'Cython'
      ],
      keywords = [],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering',
      ],
     )
