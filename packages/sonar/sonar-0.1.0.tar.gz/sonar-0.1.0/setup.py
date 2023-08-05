import os
from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

version = {}
with open(os.path.join('sonar', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name="sonar",
    version=version['__version__'],
    description='Tool to profile usage of HPC resources by regularly probing processes using ps.',
    url='https://github.com/uit-no/sonar',
    maintainer='Radovan Bast',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={'console_scripts': ['sonar = sonar.cli:main']},
    install_requires=[
        'flask==1.0.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
