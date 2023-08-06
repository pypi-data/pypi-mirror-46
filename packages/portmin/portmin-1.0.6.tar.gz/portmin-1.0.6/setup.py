from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import build_ext
import numpy

with open("README.md", "r") as fh:
    long_description = fh.read()

src_dir = 'portmin'

ext = Extension(src_dir + '.optimization',
                [src_dir + '/optimization.pyx'],
                libraries=[],
                include_dirs=[numpy.get_include()])

setup(
      name="portmin",
      version="1.0.6",
      author="Meshcheryakov A. Georgy",
      author_email="metsheryakov_ga@spbstu.ru",
      description="PORT unconstrained optimization routines wrapper.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://bitbucket.org/herrberg/portmin/",
      install_requires=['numpy', 'Cython'],
      ext_modules=[ext],
      packages=find_packages(),
      cmdclass={'build_ext': build_ext},
      data_files=[('pxd', [src_dir + '/optimization.pxd']),
                  ('c', [src_dir + '/toms611.c'])],
      zip_safe=False,
      classifiers=(
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent"))
