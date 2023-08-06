from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import re
import numpy

VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
VERSIONFILE = "mdio/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))

with open("README.md", "r") as f:
    long_description = f.read()

extensions = [Extension(
        name="mdio.xtcutils",
        sources=["mdio/src/xtcutils.pyx"],
        include_dirs=[numpy.get_include()],
        )
    ]
setup(
    name = 'mdio',
    version = verstr,
    author = 'Charlie Laughton',
    author_email = 'charles.laughton@nottingham.ac.uk',
    description = 'Basic I/O for MD trajectory files',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://bitbucket.org/claughton/mdio',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
    ],
    packages = find_packages(),
    ext_modules = cythonize(extensions),
    install_requires = [
        'numpy',
        'cython',
        'netCDF4',
        'scipy',
    ],
)
