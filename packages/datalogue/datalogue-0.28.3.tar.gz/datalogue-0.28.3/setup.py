import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datalogue",
    version='0.28.3',
    author="Datalogue",
    author_email="info@datalogue.io",
    description="Datalogue SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["pytest", "pyarrow", "validators", "python-dateutil", "numpy", "pyyaml", "requests"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
