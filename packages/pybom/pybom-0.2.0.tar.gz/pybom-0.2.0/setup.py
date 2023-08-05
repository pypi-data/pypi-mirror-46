import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybom",
    version="0.2.0",
    author="James Hochadel",
    author_email="james@carbonrelay.com",
    description="Generate a bill of materials and vulnerability information for your python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonrelay/pybom",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
