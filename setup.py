#!/usr/bin/env python
from setuptools import setup, find_packages

version = '0.1.5dev'

REQUIREMENTS = [
        'SQLAlchemy>=0.7.8',
        ]

setup(name = 'ordenley',
      version = version,
      long_description = open('README.rst').read(),
      author = 'Oscar Ramirez',
      author_email = 'tuxskar@gmail.com',
      description = 'Manager desktop app oriented to lawyers office',
      license = 'GPLv3',
      url = 'http://github.com/tuxskar/ord-en-ley',
      packages = find_packages(),
      data_files = [
          ('ordenley/interfaces' , ['ordenley/views/interfaces/main_view.glade',
              'ordenley/views/interfaces/client_view.glade']),
            ],
      install_requires = REQUIREMENTS,
      entry_points = {
          'console_scripts':
          ['ordenley = ordenley.test.run:main']
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
