#!/usr/bin/env python

from setuptools import setup, find_packages
version='0.1dev'
REQUIREMENTS = [
        'SQLAechemy>=0.7.8',
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
      packages=find_packages(),
      data_files=[('interfaces', [
            'src/interfaces/client_view.glade',
            'src/interfaces/main_view.glade',
            ])],
      license='GPLv3',
      entry_points={
          'console_scripts':
          ['ordenley = src.test.run:main']
          },
      install_requires=REQUIREMENTS
     )
