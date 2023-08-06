import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schistoscope",
    version="0.0.1",
    author="Samuel Kernan Freire",
    author_email="skernanfreire@gmail.com",
    description="Schistoscope RPi software package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jerzeek/schistoscope",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)