import sys
import os
# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'mri10yr06mo01da_normal',
      version          =   '1.1.2',
      description      =   'An anonymized MRI exemplar', 
      long_description =   readme(),
      author           =   'Rudolph Pienaar',
      author_email     =   'rudolph.pienaar@gmail.com',
      url              =   'https://github.com/FNNDSC/pl-mri10yr06mo01da_normal',
      packages         =   ['mri10yr06mo01da_normal'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['mri10yr06mo01da_normal/mri10yr06mo01da_normal.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
