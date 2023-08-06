import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTelnet",
    version="1.0.1",
    author="Silvan Kohler",
    author_email="edu.silvan.kohler@gmail.com",
    description="A small package for sending and recieving commands per tcp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SilvanKohler/PyTelnet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)