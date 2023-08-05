import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysqlsync",
    version="1.0.1",
    author="Harish U Warrier",
    author_email="huwz1it@gmail.com",
    description="A package to sync mysql from json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harishuw/mysqlsync",
	install_requires=['mysql-connector-python'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)