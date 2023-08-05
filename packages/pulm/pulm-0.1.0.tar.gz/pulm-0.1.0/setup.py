import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulm",
    version="0.1.0",
    author="Julien Jerphanion",
    author_email="git@jjerphan.xyz",
    description="UML diagram generator 🛩",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjerphan/pulm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
