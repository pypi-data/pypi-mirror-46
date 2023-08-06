import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="akamaiclient",
    version="0.1.2",
    author="Damián Valderrama",
    author_email="damianvalderrama@gmail.com",
    description="AKAMAI API 2.0 Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/chechenio/akamaiclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
