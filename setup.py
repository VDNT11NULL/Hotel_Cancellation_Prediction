from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Hotel-Cancellation-MLOps1",
    version="0.0.1",
    author="VDNT",
    packages=find_packages(),
    install_requires = requirements,
)