from setuptools import setup, find_packages

setup(
    name = "theia",
    version = "0.0.0",
    author = "R. Duque",
    url="",
    author_email = "raphael.duque@polytechnique.edu",
      packages = find_packages(exclude='test'),
    install_requires = ['numpy>=1.5.0', 'freecad>=0.1.0'],
)

