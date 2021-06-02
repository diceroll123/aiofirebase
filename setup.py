"""Setup script."""
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='aiofirebase',
    version='0.2.0',
    packages=find_packages(),
    description='Asyncio Firebase client library',
    author='Billy Shambrook',
    author_email='billy.shambrook@gmail.com',
    install_requires=requirements,
    keywords=['firebase', 'asyncio', 'aiohttp'],
    url='https://github.com/billyshambrook/aiofirebase'
)
