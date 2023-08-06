from setuptools import setup, Extension

setup(
    name = 'bruce-package',
    version = '0.5',
    description = 'GPU-accelerated binary star model',
    url = None,
    author = 'Samuel Gill et al',
    author_email = 'samuel.gill@warwick.ac.uk',
    license = 'GNU',
    packages=['bruce','bruce/binarystar'],
    scripts=['ngtsfit/ngtsfit'],
    install_requires=['celerite', 'numba', 'numpy', 'emcee']
)