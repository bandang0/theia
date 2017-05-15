from setuptools import setup, find_packages

setup(
	#General
    name = "theia",
    version = "0.0.0",
    author = "R. Duque",
    description = "3D Gaussian beam tracing and visualization",
	license = "GNU GPLv3",

	#Requires and entries
    packages = find_packages(exclude='tests'),
    install_requires = ['numpy>=1.5.0'],
	scripts = ['bin/theia'],
	
	#Metadata
    author_email = "raphael.duque@polytechnique.edu"
)

