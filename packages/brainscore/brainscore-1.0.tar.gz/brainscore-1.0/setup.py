import os
from setuptools import setup, find_packages
#from distutils.core import setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='brainscore',
    version='1.0',
    #packages=[],

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    # url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/gcpds/python-brainscore/downloads/',

    install_requires=['openbci',
                      # 'python-for-android', #install from git
                      ],

    include_package_data=True,
    license='BSD License',
    description="BrainScore: .",
    #    long_description = README,

    classifiers=[

    ],

)
