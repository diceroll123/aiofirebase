"""Setup script."""
from setuptools import find_packages
from setuptools import setup


setup(
    name='aiofirebase',
    version='0.1.0',
    packages=find_packages(),
    description='Asyncio Firebase client library',
    author='Billy Shambrook',
    email='billy.shambrook@gmail.com',
    install_requires=['aiohttp'],
    keywords=['firebase', 'asyncio', 'aiohttp'],
    url='https://github.com/billyshambrook/aiofirebase'
)
