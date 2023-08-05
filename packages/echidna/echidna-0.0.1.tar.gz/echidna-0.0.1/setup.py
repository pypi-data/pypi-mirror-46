import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="echidna",
    version="0.0.1",
    author="1ntegrale9",
    author_email="1ntegrale9uation@gmail.com",
    description="BOT and CLI framework for handling multiple services in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1ntegrale9/echidna",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
