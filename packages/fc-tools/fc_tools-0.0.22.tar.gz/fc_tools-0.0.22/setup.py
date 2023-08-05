from setuptools import setup, find_packages
from os import path
import sys
here = path.abspath(path.dirname(__file__))


if sys.version_info[0]>2:
  with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
else:    
  with open(path.join(here, 'README.rst')) as f:  
    long_description = f.read().decode("UTF-8")


setup_defaults = {  
   'name'        : 'fc_tools',
   'description' : 'Some functions used in fc_hypermesh, fc_bench, fc_simesh, ... packages',
   'version'     : '0.0.22',
   'url'         : 'http://www.math.univ-paris13.fr/~cuvelier/software',
   'author'      : 'Francois Cuvelier',
   'author_email': 'cuvelier@math.univ-paris13.fr',
   'license'     : 'BSD',
   'packages'    : ['fc_tools'],
   'classifiers':['Topic :: Scientific/Engineering :: Mathematics'],
   } 

fc_install_requires=[] # automaticaly written by setpackages.py script

setup(name=setup_defaults['name'],
      description = setup_defaults['description'],
      long_description=long_description,
      version=setup_defaults['version'],
      url=setup_defaults['url'],
      author=setup_defaults['author'],
      author_email=setup_defaults['author_email'],
      license = setup_defaults['license'],
      packages=setup_defaults['packages'],
      classifiers=setup_defaults['classifiers'],
      install_requires=['numpy','screeninfo','appdirs','pillow','matplotlib']+ fc_install_requires     
     )
