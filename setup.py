#!/usr/bin/env python

from setuptools import setup, find_packages
version='0.1dev'
REQUIREMENTS = [
        'SQLAechemy>=0.7.8',
        'pygtk',
        ]
with open('README') as file:
    long_description = file.read()

setup(name='ord-en-ley',
      version=version,
      long_description=long_description,
      author='Oscar Ramirez',
      author_email='tuxskar@gmail.com',
      description='Manager desktop app oriented to lawyers office',
      license='GPLv3',
      url='http://github.com/tuxskar/ord-en-ley',
      packages=find_packages(),
      data_files=[('interfaces', [
            'src/interfaces/client_view.glade',
            'src/interfaces/main_view.glade',
            ])],
      install_requires=REQUIREMENTS
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python :: 2.7',
          ]
      entry_points={
          'console_scripts':
          ['ordenley = src.test.run:main']
          },
     )
