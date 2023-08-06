# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join
from os import walk

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

c_files = []
for (dirpath, dirs, files) in walk('valiml'):
    for fname in files:
        if (fname.endswith('.c') or fname.endswith('.h')) and not fname.startswith('_cffi_'):
            c_files.append(join(dirpath, fname))

setup(
    name="valiml",
    version="0.1.5",
    description="Extension of sklearn with tweaked implementation of common machine learning algorithms for self-use.",
    license="MIT",
    author="Valentin-Bogdan Roșca",
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    setup_requires=["cffi"],
    install_requires=["cffi"],
    cffi_modules=[join('valiml', 'utils', 'src', 'cffi.py:ffibuilder')],
    package_data={
        '': ['*.h', '*.c']
    },
    include_package_data=True,
    data_files=[('.', c_files)],
    zip_safe=True
)
