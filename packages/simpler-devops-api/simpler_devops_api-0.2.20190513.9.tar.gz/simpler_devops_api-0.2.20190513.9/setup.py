import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpler_devops_api",
    version="0.2." + os.environ.get('BUILD_BUILDNUMBER'),
    author="Jon Truran",
    author_email="jontruran@paypoint.com",
    description="A Simpler Python Module for interacting with Azure Devops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/JonTruran/python-devops/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
