
from setuptools import setup, find_packages

setup(
    name="hub2slack",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pytest==3.5.0",
        "pytest-aiohttp",
        "aiohttp",
    ],
)

