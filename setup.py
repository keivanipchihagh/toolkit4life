from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "toolkit4life",                                      # This is the name of the package
    version = "0.1.19",                                         # The initial release version
    author = "Keivan Ipchi Hagh",                               # Full name of the author
    url = "https://github.com/keivanipchihagh/toolkit4life",    # URL to the github repository
    description = "Faster deployment is what we want!",
    long_description = long_description,                        # Long description read from the the readme file
    long_description_content_type = "text/markdown",
    packages = find_namespace_packages(include = ["toolkit4life", "toolkit4life.*"]),   # List of all python modules to be installed
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                                          # Information to filter the project on PyPi website
    python_requires = '>=3.6',                                  # Minimum version requirement of the package
    py_modules = ["toolkit4life"],                              # Name of the python package
    # package_dir = {'':'toolkit4life'},                        # Directory of the source code of the package
    install_requires = required                                 # Install other dependencies if any
)