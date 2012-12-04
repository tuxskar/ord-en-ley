#!/usr/bin/env python

from distutils.core import setup
version='0.1dev'
REQUIREMENTS = [
        'SQLAlchemy>=0.7.8',
        'pygtk',
        ]
with open('README') as file:
    long_description = file.read()

setup(name='Ord-en Ley',
      version=version,
      description='Manager desktop app oriented to lawyers office',
      long_description=long_description,
      author='Oscar Ramirez',
      author_email='tuxskar@gmail.com',
      url='http://github.com/tuxskar/ord-en-ley',
      packages=['controllers','db','models','views'],
      data_files=[('interfaces', [
            'interfaces/client_view.glade',
            'interfaces/main_view.glade',
            ])]
      license='GNUv3',
      install_requires=REQUIREMENTS
     )
