import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleGP",
    version="0.1",
    author="Marco Virgolin",
    author_email="marco.virgolin@gmail.com",
    description="Simple genetic programming for symbolic regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcovirgolin/simplegp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
