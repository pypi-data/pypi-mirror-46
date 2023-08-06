import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

print(setuptools.find_packages("senselyClinet"))


setuptools.setup(
    name="senselyClient",
    version="0.0.13",
    author="Sensely.in",
    author_email="mail@sensely.in",
    description="A library to send data stream for ingestion and analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/readall/senselyClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
