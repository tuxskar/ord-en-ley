#!/usr/bin/env python
from setuptools import setup, find_packages
#from distutils.core import setup

version = '0.1dev'

REQUIREMENTS = [
        'SQLAechemy>=0.7.8',
        'Pygtk',
        ]

setup(name = 'Ord-en Ley',
      version = version,
      long_description = open('README').read(),
      author = 'Oscar Ramirez',
      author_email = 'tuxskar@gmail.com',
      description = 'Manager desktop app oriented to lawyers office',
      license = 'GPLv3',
      url = 'http://github.com/tuxskar/ord-en-ley',
      packages = find_packages(),
      data_files = [
          ('interfaces' , ['main_view.glade','client_view.glade']),
            ],
      include_package_data=True,
      install_requires = REQUIREMENTS,
      entry_points = {
          'console_scripts':
          ['ordenley = src.test.run:main']
          },
      classifiers = [
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 2.7',
          ],
     )
