import os
from setuptools import setup


def read(fname: str) -> str:
    """Reads README file
    Args:
        fname (str): path to readme file
    Returns:
        str: contents in readme
    """
    full_path = os.path.join(os.path.dirname(__file__), fname)
    with open(full_path, encoding="utf-8") as file:
        return file.read()


setup(
    name="Stock-Predictor-Feature-Store",
    version="0.0.1",
    author="Marcus Allen",
    author_email="marcusCallen24@gmail.com",
    url="https://github.com/marcus-24/Stock-Predictor-Feature-Store",
    long_description=read("README.md"),
    packages=["myfeatures"],  # define package names
    package_dir={"myfeatures": "./myfeatures"},  # show where packages are stored
    install_requires=[
        "hopsworks[python]>=4.1.8",
        "holidays>=0.68",
        "pandas<2.0.0",
        "twofish",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.5",
        ]
    },  # i.e.: pip install stockfeatures[dev]
)
