import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="synode",
    version="0.1.2",
    author="Youngsung Kim",
    author_email="grnydawn@gmail.com",
    description="Syntax node Python library for programming languages",
    long_description=long_description,
    py_modules=["synode"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
