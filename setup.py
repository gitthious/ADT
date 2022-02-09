# -*- coding: utf-8 -*-
# read https://packaging.python.org/tutorials/packaging-projects/
# make sure you installed twine package with pip install twine
# run it with:
#   setup.py sdist bdist_wheel
# and upload it with:
#   python3 -m twine upload  dist/*


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ADTthious", # because ADT already exist
    version="0.5",
    description='Abstract Data Types for python',
    author='Thierry Hervé',
    author_email='thious.rv@gmail.com',
    url="https://github.com/gitthious/ADT.git",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['ADT',], # setuptools.find_packages(),
    package_dir={'ADT': '', },
    package_data={
      'ADT': ['README.md', 'calendar.png', 'Class instance of Type.ipynb' ],
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        'colour==0.1.5',
        'PySimpleGUI==4.0.0',
        'pipe==1.6.0',
        'python-dateutil==2.8.1',
    ],      
)

