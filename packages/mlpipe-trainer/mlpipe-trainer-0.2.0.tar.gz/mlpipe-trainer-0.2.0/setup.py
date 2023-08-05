from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mlpipe-trainer',
    version='0.2.0',
    author="Johannes Dobler",
    author_email="jdobler@protonmail.com",
    description="Manage training results, weights and data flow of your Tensorflow models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j-o-d-o/MLPipe-Trainer",
    install_requires=[  
        'numpy>=1.16.0',
        'pymongo>=3.7.0',
        'hdf5>=1.10.0',
        'h5py>=2.9.0',
        'redis>=5.0.0',
        'namedlist>=1.7'
        'tensorflow==2.0.0-alpha0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research'
    ],
    packages=find_packages())
