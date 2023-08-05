from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'remember', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='python-remember',
    version=version['__version__'],
    description=(' '),
    author=' ',
    author_email=' ',
    url=' ',
    license='MPL-2.0',
    packages=['remember'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
)
