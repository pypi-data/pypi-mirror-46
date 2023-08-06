"""
Py-Scripts

python scripts for any platforms, includes `py_replace`.

"""
from __future__ import absolute_import, division, print_function
from setuptools import setup
import py_scripts

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="py_scripts",
    url="https://github.com/dodoru/py_scripts",
    license="MIT",
    version=py_scripts.__version__,
    author=py_scripts.__author__,
    author_email=py_scripts.__author_email__,
    description=py_scripts.__doc__,
    long_description=readme,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    packages=["py_scripts"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],

    entry_points={
        'console_scripts': [
            'py_replace = py_scripts.py_replace:cli',
        ],
    },
    install_requires=["click"],
    platforms='any',
)
