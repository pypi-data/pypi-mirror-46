#coding = utf-8
from setuptools import setup, find_namespace_packages

setup(
    name="treelab",
    version="1.2.0",
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    install_requires=['Rx>=3.0.0a3', 'grpcio>=1.20.0', 'grpcio-tools>=1.20.0', 'pandas>=0.24.2'],
    python_requires='>=3',
    license='BSD License',
    url='https://github.com/caminerinc/treelab-pySDK',
    long_description='The Treelab Python API provides an easy way to integrate Treelab with any external system. The API closely follows REST semantics, uses JSON to encode objects, and relies on standard HTTP codes to signal operation outcomes.'
)
